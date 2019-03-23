package main

import "errors"

var (
	ErrSnippetTitleDuplicated = errors.New("")
	ErrPostTagDuplicated      = errors.New("Tag name already exists")

	ErrBadRequest     = errors.New("Invalid request.")
	ErrUnauthorized   = errors.New("Unauthorized.")
	ErrForbidden      = errors.New("Operation not permitted.")
	ErrInternalServer = errors.New("Unexpected error. Please retry later.")
)
