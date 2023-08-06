from cerver.utils.log import LOG_TYPE_NONE, cerver_log_both

from .lib import lib

SILVERSE_VERSION = "0.1"
SILVERSE_VERSION_NAME = "Version 0.1"
SILVERSE_VERSION_DATE = "30/03/2023"
SILVERSE_VERSION_TIME = "22:50 CST"
SILVERSE_VERSION_AUTHOR = "Erick Salas"

version = {
	"id": SILVERSE_VERSION,
	"name": SILVERSE_VERSION_NAME,
	"date": SILVERSE_VERSION_DATE,
	"time": SILVERSE_VERSION_TIME,
	"author": SILVERSE_VERSION_AUTHOR
}

silverse_libauth_version_print_full = lib.silverse_libauth_version_print_full
silverse_libauth_version_print_version_id = lib.silverse_libauth_version_print_version_id
silverse_libauth_version_print_version_name = lib.silverse_libauth_version_print_version_name

def pysilverse_version_print_full ():
	output = "\nPySilverse Version: {name}\n" \
		"Release Date: {date} - {time}\n" \
		"Author: {author}\n".format (**version)

	cerver_log_both (
		LOG_TYPE_NONE, LOG_TYPE_NONE,
		output.encode ("utf-8")
	)

def pysilverse_version_print_version_id ():
	cerver_log_both (
		LOG_TYPE_NONE, LOG_TYPE_NONE,
		f"\nPySilverse Version ID: {version.id}\n".encode ("utf-8")
	)

def pysilverse_version_print_version_name ():
	cerver_log_both (
		LOG_TYPE_NONE, LOG_TYPE_NONE,
		f"\nPySilverse Version: {version.name}\n".encode ("utf-8")
	)
