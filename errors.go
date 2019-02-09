package main

import "errors"

var (
	ErrPostTagDuplicated = errors.New("Tag name already exists")

	ErrBadRequest = errors.New("Invalid request.")
	ErrInternalServer = errors.New("Unexpected error. Please retry later.")
)
