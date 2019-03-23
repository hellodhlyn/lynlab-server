package main

import (
	"github.com/graphql-go/graphql"
)

const (
	enumSortDirectionAsc = iota
	enumSortDirectionDesc
)

var pageSortDirectionEnum = graphql.NewEnum(graphql.EnumConfig{
	Name: "SortDirection",
	Values: graphql.EnumValueConfigMap{
		"ASC":  &graphql.EnumValueConfig{Value: enumSortDirectionAsc},
		"DESC": &graphql.EnumValueConfig{Value: enumSortDirectionDesc},
	},
})

var pageArguments = graphql.ArgumentConfig{
	Type: graphql.NewInputObject(graphql.InputObjectConfig{
		Name: "PageInput",
		Fields: graphql.InputObjectConfigFieldMap{
			"after":         &graphql.InputObjectFieldConfig{Type: graphql.Int},
			"before":        &graphql.InputObjectFieldConfig{Type: graphql.Int},
			"count":         &graphql.InputObjectFieldConfig{Type: graphql.Int, DefaultValue: 20},
			"sortDirection": &graphql.InputObjectFieldConfig{Type: pageSortDirectionEnum, DefaultValue: enumSortDirectionDesc},
		},
	}),
	DefaultValue: map[string]interface{}{
		"count":         20,
		"sortDirection": "DESC",
	},
}

type pageInfo struct {
	HasBefore bool
	HasNext   bool
}

func pageTypeOf(typ graphql.Type) *graphql.Object {
	return graphql.NewObject(graphql.ObjectConfig{
		Name: typ.Name() + "Page",
		Fields: graphql.Fields{
			"items": &graphql.Field{Type: NonNullListOf(typ)},
			"pageInfo": &graphql.Field{Type: graphql.NewNonNull(
				graphql.NewObject(graphql.ObjectConfig{
					Name: "PageInfo",
					Fields: graphql.Fields{
						"hasBefore": &graphql.Field{Type: graphql.NewNonNull(graphql.Boolean)},
						"hasNext":   &graphql.Field{Type: graphql.NewNonNull(graphql.Boolean)},
					},
				}),
			)},
		},
	})
}