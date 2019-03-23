package main

import (
	"time"

	cachelib "github.com/patrickmn/go-cache"
)

var cache = cachelib.New(24*time.Hour, 1*time.Hour)
