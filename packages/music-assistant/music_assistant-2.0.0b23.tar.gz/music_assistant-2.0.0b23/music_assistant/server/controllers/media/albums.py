"""Manage MediaItems of type Album."""
from __future__ import annotations

import asyncio
import contextlib
from random import choice, random
from typing import TYPE_CHECKING

from music_assistant.common.helpers.datetime import utc_timestamp
from music_assistant.common.helpers.json import serialize_to_json
from music_assistant.common.models.enums import EventType, ProviderFeature
from music_assistant.common.models.errors import MediaNotFoundError, UnsupportedFeaturedException
from music_assistant.common.models.media_items import (
    Album,
    AlbumType,
    Artist,
    DbAlbum,
    ItemMapping,
    MediaType,
    Track,
)
from music_assistant.constants import DB_TABLE_ALBUMS, DB_TABLE_TRACKS, VARIOUS_ARTISTS
from music_assistant.server.controllers.media.base import MediaControllerBase
from music_assistant.server.helpers.compare import compare_album, loose_compare_strings

if TYPE_CHECKING:
    from music_assistant.server.models.music_provider import MusicProvider


class AlbumsController(MediaControllerBase[Album]):
    """Controller managing MediaItems of type Album."""

    db_table = DB_TABLE_ALBUMS
    media_type = MediaType.ALBUM
    item_cls = DbAlbum

    def __init__(self, *args, **kwargs):
        """Initialize class."""
        super().__init__(*args, **kwargs)
        # register api handlers
        self.mass.register_api_command("music/albums", self.db_items)
        self.mass.register_api_command("music/album", self.get)
        self.mass.register_api_command("music/album/tracks", self.tracks)
        self.mass.register_api_command("music/album/versions", self.versions)
        self.mass.register_api_command("music/album/update", self._update_db_item)
        self.mass.register_api_command("music/album/delete", self.delete)

    async def get(
        self,
        item_id: str,
        provider_instance_id_or_domain: str,
        force_refresh: bool = False,
        lazy: bool = True,
        details: Album = None,
        add_to_db: bool = True,
    ) -> Album:
        """Return (full) details for a single media item."""
        album = await super().get(
            item_id,
            provider_instance_id_or_domain,
            force_refresh=force_refresh,
            lazy=lazy,
            details=details,
            add_to_db=add_to_db,
        )
        # append full artist details to full album item
        album.artists = [
            await self.mass.music.artists.get(
                item.item_id,
                item.provider,
                lazy=True,
                details=item,
                add_to_db=add_to_db,
            )
            for item in album.artists
        ]
        return album

    async def add(self, item: Album, skip_metadata_lookup: bool = False) -> Album:
        """Add album to local db and return the database item."""
        # resolve any ItemMapping artists
        item.artists = [
            await self.mass.music.artists.get_provider_item(artist.item_id, artist.provider)
            if isinstance(artist, ItemMapping)
            else artist
            for artist in item.artists
        ]
        # grab additional metadata
        if not skip_metadata_lookup:
            await self.mass.metadata.get_album_metadata(item)
        existing = await self.get_db_item_by_prov_id(item.item_id, item.provider)
        if existing:
            db_item = await self._update_db_item(existing.item_id, item)
        else:
            db_item = await self._add_db_item(item)
        # also fetch the same album on all providers
        if not skip_metadata_lookup:
            await self._match(db_item)
        # return final db_item after all match/metadata actions
        db_item = await self.get_db_item(db_item.item_id)
        # preload album tracks in db
        for prov_mapping in db_item.provider_mappings:
            for track in await self._get_provider_album_tracks(
                prov_mapping.item_id, prov_mapping.provider_instance
            ):
                if not await self.mass.music.tracks.get_db_item_by_prov_id(
                    track.item_id, track.provider
                ):
                    await self.mass.music.tracks.add(track, skip_metadata_lookup=True)
        self.mass.signal_event(
            EventType.MEDIA_ITEM_UPDATED if existing else EventType.MEDIA_ITEM_ADDED,
            db_item.uri,
            db_item,
        )
        return db_item

    async def delete(self, item_id: int, recursive: bool = False) -> None:
        """Delete record from the database."""
        # check album tracks
        db_rows = await self.mass.music.database.get_rows_from_query(
            f"SELECT item_id FROM {DB_TABLE_TRACKS} WHERE albums LIKE '%\"{item_id}\"%'",
            limit=5000,
        )
        assert not (db_rows and not recursive), "Tracks attached to album"
        for db_row in db_rows:
            with contextlib.suppress(MediaNotFoundError):
                await self.mass.music.tracks.delete(db_row["item_id"], recursive)

        # delete the album itself from db
        await super().delete(item_id)

    async def tracks(
        self,
        item_id: str,
        provider_instance_id_or_domain: str,
    ) -> list[Track]:
        """Return album tracks for the given provider album id."""
        if provider_instance_id_or_domain == "database":
            if db_result := await self._get_db_album_tracks(item_id):
                return db_result
            # no results in db (yet), grab provider details
            if db_album := await self.get_db_item(item_id):
                for prov_mapping in db_album.provider_mappings:
                    # returns the first provider that is available
                    if not prov_mapping.available:
                        continue
                    return await self._get_provider_album_tracks(
                        prov_mapping.item_id, prov_mapping.provider_instance
                    )

        # return provider album tracks
        return await self._get_provider_album_tracks(item_id, provider_instance_id_or_domain)

    async def versions(
        self,
        item_id: str,
        provider_instance_id_or_domain: str,
    ) -> list[Album]:
        """Return all versions of an album we can find on all providers."""
        album = await self.get(item_id, provider_instance_id_or_domain, add_to_db=False)
        # perform a search on all provider(types) to collect all versions/variants
        search_query = f"{album.artists[0].name} - {album.name}"
        all_versions = {
            prov_item.item_id: prov_item
            for prov_items in await asyncio.gather(
                *[
                    self.search(search_query, provider_instance_id)
                    for provider_instance_id in self.mass.music.get_unique_providers()
                ]
            )
            for prov_item in prov_items
            if loose_compare_strings(album.name, prov_item.name)
        }
        # make sure that the 'base' version is NOT included
        for prov_version in album.provider_mappings:
            all_versions.pop(prov_version.item_id, None)

        # return the aggregated result
        return all_versions.values()

    async def _add_db_item(self, item: Album) -> Album:
        """Add a new record to the database."""
        assert item.provider_mappings, "Item is missing provider mapping(s)"
        assert item.artists, f"Album {item.name} is missing artists"
        async with self._db_add_lock:
            cur_item = None
            # always try to grab existing item by musicbrainz_id
            if item.musicbrainz_id:
                match = {"musicbrainz_id": item.musicbrainz_id}
                cur_item = await self.mass.music.database.get_row(self.db_table, match)
            # try barcode/upc
            if not cur_item and item.barcode:
                for barcode in item.barcode:
                    if search_result := await self.mass.music.database.search(
                        self.db_table, barcode, "barcode"
                    ):
                        cur_item = Album.from_db_row(search_result[0])
                        break
            if not cur_item:
                # fallback to search and match
                for row in await self.mass.music.database.search(self.db_table, item.name):
                    row_album = Album.from_db_row(row)
                    if compare_album(row_album, item):
                        cur_item = row_album
                        break
            if cur_item:
                # update existing
                return await self._update_db_item(cur_item.item_id, item)

            # insert new item
            album_artists = await self._get_album_artists(item, cur_item)
            sort_artist = album_artists[0].sort_name if album_artists else ""
            new_item = await self.mass.music.database.insert(
                self.db_table,
                {
                    **item.to_db_row(),
                    "artists": serialize_to_json(album_artists) or None,
                    "sort_artist": sort_artist,
                    "timestamp_added": int(utc_timestamp()),
                    "timestamp_modified": int(utc_timestamp()),
                },
            )
            item_id = new_item["item_id"]
            # update/set provider_mappings table
            await self._set_provider_mappings(item_id, item.provider_mappings)
            self.logger.debug("added %s to database", item.name)
            # return created object
            return await self.get_db_item(item_id)

    async def _update_db_item(
        self,
        item_id: int,
        item: Album,
    ) -> Album:
        """Update Album record in the database."""
        assert item.provider_mappings, "Item is missing provider mapping(s)"
        assert item.artists, f"Album {item.name} is missing artist"
        cur_item = await self.get_db_item(item_id)
        is_file_provider = item.provider.startswith("filesystem")
        metadata = cur_item.metadata.update(item.metadata, is_file_provider)
        provider_mappings = {*cur_item.provider_mappings, *item.provider_mappings}
        if is_file_provider:
            album_artists = await self._get_album_artists(cur_item)
        else:
            album_artists = await self._get_album_artists(cur_item, item)
        cur_item.barcode.update(item.barcode)
        if item.album_type != AlbumType.UNKNOWN:
            album_type = item.album_type
        else:
            album_type = cur_item.album_type

        sort_artist = album_artists[0].sort_name if album_artists else ""

        await self.mass.music.database.update(
            self.db_table,
            {"item_id": item_id},
            {
                "name": item.name if is_file_provider else cur_item.name,
                "sort_name": item.sort_name if is_file_provider else cur_item.sort_name,
                "sort_artist": sort_artist,
                "version": item.version if is_file_provider else cur_item.version,
                "year": item.year or cur_item.year,
                "barcode": ";".join(cur_item.barcode),
                "album_type": album_type.value,
                "artists": serialize_to_json(album_artists) or None,
                "metadata": serialize_to_json(metadata),
                "provider_mappings": serialize_to_json(provider_mappings),
                "musicbrainz_id": item.musicbrainz_id or cur_item.musicbrainz_id,
                "timestamp_modified": int(utc_timestamp()),
            },
        )
        # update/set provider_mappings table
        await self._set_provider_mappings(item_id, provider_mappings)
        self.logger.debug("updated %s in database: %s", item.name, item_id)
        return await self.get_db_item(item_id)

    async def _get_provider_album_tracks(
        self, item_id: str, provider_instance_id_or_domain: str
    ) -> list[Track]:
        """Return album tracks for the given provider album id."""
        assert provider_instance_id_or_domain != "database"
        prov = self.mass.get_provider(provider_instance_id_or_domain)
        if prov is None:
            return []

        full_album = await self.get_provider_item(item_id, provider_instance_id_or_domain)
        # prefer cache items (if any)
        cache_key = f"{prov.instance_id}.albumtracks.{item_id}"
        cache_checksum = full_album.metadata.checksum
        if cache := await self.mass.cache.get(cache_key, checksum=cache_checksum):
            return [Track.from_dict(x) for x in cache]
        # no items in cache - get listing from provider
        items = []
        for track in await prov.get_album_tracks(item_id):
            # make sure that the (full) album is stored on the tracks
            track.album = full_album
            if full_album.metadata.images:
                track.metadata.images = full_album.metadata.images
            items.append(track)
        # store (serializable items) in cache
        self.mass.create_task(
            self.mass.cache.set(cache_key, [x.to_dict() for x in items], checksum=cache_checksum)
        )
        return items

    async def _get_provider_dynamic_tracks(
        self,
        item_id: str,
        provider_instance_id_or_domain: str,
        limit: int = 25,
    ):
        """Generate a dynamic list of tracks based on the album content."""
        assert provider_instance_id_or_domain != "database"
        prov = self.mass.get_provider(provider_instance_id_or_domain)
        if prov is None:
            return []
        if ProviderFeature.SIMILAR_TRACKS not in prov.supported_features:
            return []
        album_tracks = await self._get_provider_album_tracks(
            item_id, provider_instance_id_or_domain
        )
        # Grab a random track from the album that we use to obtain similar tracks for
        track = choice(album_tracks)
        # Calculate no of songs to grab from each list at a 10/90 ratio
        total_no_of_tracks = limit + limit % 2
        no_of_album_tracks = int(total_no_of_tracks * 10 / 100)
        no_of_similar_tracks = int(total_no_of_tracks * 90 / 100)
        # Grab similar tracks from the music provider
        similar_tracks = await prov.get_similar_tracks(
            prov_track_id=track.item_id, limit=no_of_similar_tracks
        )
        # Merge album content with similar tracks
        # ruff: noqa: ARG005
        dynamic_playlist = [
            *sorted(album_tracks, key=lambda n: random())[:no_of_album_tracks],
            *sorted(similar_tracks, key=lambda n: random())[:no_of_similar_tracks],
        ]
        return sorted(dynamic_playlist, key=lambda n: random())

    async def _get_dynamic_tracks(
        self, media_item: Album, limit: int = 25  # noqa: ARG002
    ) -> list[Track]:
        """Get dynamic list of tracks for given item, fallback/default implementation."""
        # TODO: query metadata provider(s) to get similar tracks (or tracks from similar artists)
        raise UnsupportedFeaturedException(
            "No Music Provider found that supports requesting similar tracks."
        )

    async def _get_db_album_tracks(
        self,
        item_id: str,
    ) -> list[Track]:
        """Return in-database album tracks for the given database album."""
        db_album = await self.get_db_item(item_id)
        # simply grab all tracks in the db that are linked to this album
        # TODO: adjust to json query instead of text search?
        query = f'SELECT * FROM {DB_TABLE_TRACKS} WHERE albums LIKE \'%"item_id":"{item_id}","provider":"database"%\''  # noqa: E501
        result = []
        for track in await self.mass.music.tracks.get_db_items_by_query(query):
            if album_mapping := next(
                (x for x in track.albums if x.item_id == db_album.item_id), None
            ):
                # make sure that the full album is set on the track and prefer the album's images
                track.album = db_album
                if db_album.metadata.images:
                    track.metadata.images = db_album.metadata.images
                # apply the disc and track number from the mapping
                track.disc_number = album_mapping.disc_number
                track.track_number = album_mapping.track_number
                result.append(track)
        return sorted(result, key=lambda x: (x.disc_number or 0, x.track_number or 0))

    async def _match(self, db_album: Album) -> None:
        """Try to find matching album on all providers for the provided (database) album.

        This is used to link objects of different providers/qualities together.
        """
        if db_album.provider != "database":
            return  # Matching only supported for database items

        async def find_prov_match(provider: MusicProvider):
            self.logger.debug(
                "Trying to match album %s on provider %s", db_album.name, provider.name
            )
            match_found = False
            for search_str in (
                db_album.name,
                f"{db_album.artists[0].name} - {db_album.name}",
                f"{db_album.artists[0].name} {db_album.name}",
            ):
                if match_found:
                    break
                search_result = await self.search(search_str, provider.instance_id)
                for search_result_item in search_result:
                    if not search_result_item.available:
                        continue
                    if not compare_album(search_result_item, db_album):
                        continue
                    # we must fetch the full album version, search results are simplified objects
                    prov_album = await self.get_provider_item(
                        search_result_item.item_id, search_result_item.provider
                    )
                    if compare_album(prov_album, db_album):
                        # 100% match, we can simply update the db with additional provider ids
                        await self._update_db_item(db_album.item_id, prov_album)
                        match_found = True
            return match_found

        # try to find match on all providers
        cur_provider_domains = {x.provider_domain for x in db_album.provider_mappings}
        for provider in self.mass.music.providers:
            if provider.domain in cur_provider_domains:
                continue
            if ProviderFeature.SEARCH not in provider.supported_features:
                continue
            if await find_prov_match(provider):
                cur_provider_domains.add(provider.domain)
            else:
                self.logger.debug(
                    "Could not find match for Album %s on provider %s",
                    db_album.name,
                    provider.name,
                )

    async def _get_album_artists(
        self,
        db_album: Album,
        updated_album: Album | None = None,
    ) -> list[ItemMapping]:
        """Extract (database) album artist(s) as ItemMapping."""
        album_artists = set()
        for album in (updated_album, db_album):
            if not album:
                continue
            for artist in album.artists:
                album_artists.add(await self._get_artist_mapping(artist))
        # use intermediate set to prevent duplicates
        # filter various artists if multiple artists
        if len(album_artists) > 1:
            album_artists = {x for x in album_artists if (x.name != VARIOUS_ARTISTS)}
        return list(album_artists)

    async def _get_artist_mapping(self, artist: Artist | ItemMapping) -> ItemMapping:
        """Extract (database) track artist as ItemMapping."""
        if artist.provider == "database":
            if isinstance(artist, ItemMapping):
                return artist
            return ItemMapping.from_item(artist)

        if db_artist := await self.mass.music.artists.get_db_item_by_prov_id(
            artist.item_id, artist.provider
        ):
            return ItemMapping.from_item(db_artist)

        db_artist = await self.mass.music.artists._add_db_item(artist)
        return ItemMapping.from_item(db_artist)
