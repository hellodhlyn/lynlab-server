package main

import "errors"

var (
	ErrPostTagDuplicated = errors.New("Tag name already exists")

	ErrInternalServer = errors.New("Unexpected error. Please retry later.")
)
