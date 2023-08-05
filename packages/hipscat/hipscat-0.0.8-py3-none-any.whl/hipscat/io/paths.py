"""Methods for creating partitioned data paths"""
from __future__ import annotations

from hipscat.io.file_io.file_pointer import FilePointer, append_paths_to_pointer

ORDER_DIRECTORY_PREFIX = "Norder"
DIR_DIRECTORY_PREFIX = "Dir"
PIXEL_DIRECTORY_PREFIX = "Npix"

CATALOG_INFO_FILENAME = "catalog_info.json"
PARTITION_INFO_FILENAME = "partition_info.csv"
PROVENANCE_INFO_FILENAME = "provenance_info.json"
PARQUET_METADATA_FILENAME = "_metadata"
PARQUET_COMMON_METADATA_FILENAME = "_common_metadata"
POINT_MAP_FILENAME = "point_map.fits"


def pixel_directory(
    catalog_base_dir: FilePointer,
    pixel_order: int,
    pixel_number: int | None = None,
    directory_number: int | None = None,
) -> FilePointer:
    """Create path pointer for a pixel directory. This will not create the directory.

    One of pixel_number or directory_number is required. The directory name will
    take the HiPS standard form of:

        <catalog_base_dir>/Norder=<pixel_order>/Dir=<directory number>

    Where the directory number is calculated using integer division as:

        (pixel_number/10000)*10000

    Args:
        catalog_base_dir (FilePointer): base directory of the catalog (includes catalog name)
        pixel_order (int): the healpix order of the pixel
        directory_number (int): directory number
        pixel_number (int): the healpix pixel
    Returns:
        FilePointer directory name
    """
    norder = int(pixel_order)
    if pixel_number is None and directory_number is None:
        raise ValueError(
            "One of pixel_number or directory_number is required to create pixel directory"
        )
    if directory_number is not None:
        ndir = directory_number
    else:
        npix = int(pixel_number)
        ndir = int(npix / 10_000) * 10_000
    return append_paths_to_pointer(
        catalog_base_dir,
        f"{ORDER_DIRECTORY_PREFIX}={norder}",
        f"{DIR_DIRECTORY_PREFIX}={ndir}",
    )


def pixel_catalog_file(
    catalog_base_dir: FilePointer, pixel_order: int, pixel_number: int
) -> FilePointer:
    """Create path *pointer* for a pixel catalog file. This will not create the directory or file.

    The catalog file name will take the HiPS standard form of:

        <catalog_base_dir>/Norder=<pixel_order>/Dir=<directory number>/Npix=<pixel_number>.parquet

    Where the directory number is calculated using integer division as:

        (pixel_number/10000)*10000

    Args:
        catalog_base_dir (FilePointer): base directory of the catalog (includes catalog name)
        pixel_order (int): the healpix order of the pixel
        pixel_number (int): the healpix pixel
    Returns:
        string catalog file name
    """
    norder = int(pixel_order)
    npix = int(pixel_number)
    ndir = int(npix / 10_000) * 10_000
    return append_paths_to_pointer(
        catalog_base_dir,
        f"{ORDER_DIRECTORY_PREFIX}={norder}",
        f"{DIR_DIRECTORY_PREFIX}={ndir}",
        f"{PIXEL_DIRECTORY_PREFIX}={npix}.parquet",
    )


def get_catalog_info_pointer(catalog_base_dir: FilePointer) -> FilePointer:
    """Get file pointer to `catalog_info.json` metadata file

    Args:
        catalog_base_dir: pointer to base catalog directory
    Returns:
        File Pointer to the catalog's `catalog_info.json` file
    """
    return append_paths_to_pointer(catalog_base_dir, CATALOG_INFO_FILENAME)


def get_partition_info_pointer(catalog_base_dir: FilePointer) -> FilePointer:
    """Get file pointer to `partition_info.csv` metadata file

    Args:
        catalog_base_dir: pointer to base catalog directory
    Returns:
        File Pointer to the catalog's `partition_info.csv` file
    """
    return append_paths_to_pointer(catalog_base_dir, PARTITION_INFO_FILENAME)


def get_provenance_pointer(catalog_base_dir: FilePointer) -> FilePointer:
    """Get file pointer to `provenance_info.json` metadata file

    Args:
        catalog_base_dir: pointer to base catalog directory
    Returns:
        File Pointer to the catalog's `provenance_info.json` file
    """
    return append_paths_to_pointer(catalog_base_dir, PROVENANCE_INFO_FILENAME)


def get_common_metadata_pointer(catalog_base_dir: FilePointer) -> FilePointer:
    """Get file pointer to `_metadata` parquet metadata file

    Args:
        catalog_base_dir: pointer to base catalog directory
    Returns:
        File Pointer to the catalog's `_metadata` file
    """
    return append_paths_to_pointer(catalog_base_dir, PARQUET_COMMON_METADATA_FILENAME)


def get_parquet_metadata_pointer(catalog_base_dir: FilePointer) -> FilePointer:
    """Get file pointer to `_common_metadata` parquet metadata file

    Args:
        catalog_base_dir: pointer to base catalog directory
    Returns:
        File Pointer to the catalog's `_common_metadata` file
    """
    return append_paths_to_pointer(catalog_base_dir, PARQUET_METADATA_FILENAME)


def get_point_map_file_pointer(catalog_base_dir: FilePointer) -> FilePointer:
    """Get file pointer to `point_map.fits` FITS image file.

    Args:
        catalog_base_dir: pointer to base catalog directory
    Returns:
        File Pointer to the catalog's `point_map.fits` FITS image file.
    """
    return append_paths_to_pointer(catalog_base_dir, POINT_MAP_FILENAME)
