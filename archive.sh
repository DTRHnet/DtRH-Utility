#!/bin/bash
#
#
#    /$$$$$$$    /$$     /$$$$$$$  /$$   /$$         /$$   /$$   /$$     /$$ /$$ /$$   /$$              
#   | $$__  $$  | $$    | $$__  $$| $$  | $$        | $$  | $$  | $$    |__/| $$|__/  | $$              
#   | $$  \ $$ /$$$$$$  | $$  \ $$| $$  | $$        | $$  | $$ /$$$$$$   /$$| $$ /$$ /$$$$$$   /$$   /$$
#   | $$  | $$|_  $$_/  | $$$$$$$/| $$$$$$$$ /$$$$$$| $$  | $$|_  $$_/  | $$| $$| $$|_  $$_/  | $$  | $$
#   | $$  | $$  | $$    | $$__  $$| $$__  $$|______/| $$  | $$  | $$    | $$| $$| $$  | $$    | $$  | $$
#   | $$  | $$  | $$ /$$| $$  \ $$| $$  | $$        | $$  | $$  | $$ /$$| $$| $$| $$  | $$ /$$| $$  | $$
#   | $$$$$$$/  |  $$$$/| $$  | $$| $$  | $$        |  $$$$$$/  |  $$$$/| $$| $$| $$  |  $$$$/|  $$$$$$$
#   |_______/    \___/  |__/  |__/|__/  |__/         \______/    \___/  |__/|__/|__/   \___/   \____  $$
#                                                                                              /$$  | $$
#   archive.sh - Create project archives                                                      |  $$$$$$/
#                                                                                              \______/ 
#   June 29, 2024
#
#                                                                                < admin [at] dtrh.net >
# ======================================================================================================



# Preset variables
__PROJECT_ROOT__="$(pwd)"
__MENU_DIR__='DtRH-menu'
__LOGGER_DIR__='DtRH-logger'
__STYLE_DIR__='DtRH-style'
__VERSION__='v0.0.2'

# Archive paths
__ARCHIVES_DIR__='archives'
__MENU_ARCHIVE_DIR__="${__ARCHIVES_DIR__}/menu"
__LOGGER_ARCHIVE_DIR__="${__ARCHIVES_DIR__}/logger"
__STYLE_ARCHIVE_DIR__="${__ARCHIVES_DIR__}/style"
__FULL_ARCHIVE_DIR__="${__ARCHIVES_DIR__}/full"

# Archive subdirectories
__ZIP_SUBDIR__='zip'
__GZIP_SUBDIR__='gzip'

# Options
VERBOSE=false
DRY_RUN=false

# Function to print help
print_help() {
    echo "Usage: $0 [options]"
    echo "Options:"
    echo "  -h, --help     Show this help message"
    echo "  -m, --menu     Create archives of menu folder"
    echo "  -l, --logger   Create archives of logger folder"
    echo "  -s, --style    Create archives of style folder"
    echo "  -a, --almost   Create archives of all folders"
    echo "  -A, --all      Create archives of all folders including root project directory"
    echo "  -v, --verbose  Enable verbose output"
    echo "  --dry-run      Perform a dry run without creating archives"
}

# Function to create archives
create_archives() {
    local src_dir=$1
    local dest_dir=$2
    local name_prefix=$3

    if [ ! -d "$src_dir" ]; then
        echo "Error: Source directory $src_dir does not exist."
        return
    fi

    local zip_file="${name_prefix}-${__VERSION__}-$(date +%m-%d-%y).zip"
    local gzip_file="${name_prefix}-${__VERSION__}-$(date +%m-%d-%y).tar.gz"

    # Check and append timestamp if file exists
    if [ -f "${dest_dir}/${__ZIP_SUBDIR__}/${zip_file}" ]; then
        zip_file="${name_prefix}-${__VERSION__}-$(date +%m-%d-%y_%H-%M).zip"
    fi
    if [ -f "${dest_dir}/${__GZIP_SUBDIR__}/${gzip_file}" ]; then
        gzip_file="${name_prefix}-${__VERSION__}-$(date +%m-%d-%y_%H-%M).tar.gz"
    fi

    if $VERBOSE; then
        echo "Creating zip archive: ${dest_dir}/${__ZIP_SUBDIR__}/${zip_file}"
        echo "Creating gzip archive: ${dest_dir}/${__GZIP_SUBDIR__}/${gzip_file}"
    fi

    if ! $DRY_RUN; then
        mkdir -p "${dest_dir}/${__ZIP_SUBDIR__}" "${dest_dir}/${__GZIP_SUBDIR__}"
        zip -r "${dest_dir}/${__ZIP_SUBDIR__}/${zip_file}" "$src_dir" > /dev/null
        tar -czf "${dest_dir}/${__GZIP_SUBDIR__}/${gzip_file}" -C "$src_dir" . > /dev/null
    fi
}

# Option parsing
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            print_help
            exit 0
            ;;
        -m|--menu)
            create_archives "$__MENU_DIR__" "$__MENU_ARCHIVE_DIR__" "$__MENU_DIR__"
            shift
            ;;
        -l|--logger)
            create_archives "$__LOGGER_DIR__" "$__LOGGER_ARCHIVE_DIR__" "$__LOGGER_DIR__"
            shift
            ;;
        -s|--style)
            create_archives "$__STYLE_DIR__" "$__STYLE_ARCHIVE_DIR__" "$__STYLE_DIR__"
            shift
            ;;
        -a|--almost)
            create_archives "$__MENU_DIR__" "$__MENU_ARCHIVE_DIR__" "$__MENU_DIR__"
            create_archives "$__LOGGER_DIR__" "$__LOGGER_ARCHIVE_DIR__" "$__LOGGER_DIR__"
            create_archives "$__STYLE_DIR__" "$__STYLE_ARCHIVE_DIR__" "$__STYLE_DIR__"
            shift
            ;;
        -A|--all)
            create_archives "." "$__FULL_ARCHIVE_DIR__" "Full-Project"
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        *)
            echo "Invalid option: $1"
            print_help
            exit 1
            ;;
    esac
done
