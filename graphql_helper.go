package main

import (
	"github.com/graphql-go/graphql"
)

func NonNullListOf(objType graphql.Type) graphql.Type {
	return graphql.NewNonNull(graphql.NewList(graphql.NewNonNull(objType)))
}
