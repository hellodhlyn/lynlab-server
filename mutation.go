package main

import (
	"github.com/graphql-go/graphql"
)

var CreatePostMutation = &graphql.Field{
	Type: graphql.NewNonNull(PostType),
	Args: graphql.FieldConfigArgument{
		"input": &graphql.ArgumentConfig{
			Type: graphql.NewInputObject(graphql.InputObjectConfig{
				Name: "CreatePostInput",
				Fields: graphql.InputObjectConfigFieldMap{
					"title":        &graphql.InputObjectFieldConfig{Type: graphql.NewNonNull(graphql.String)},
					"description":  &graphql.InputObjectFieldConfig{Type: graphql.NewNonNull(graphql.String)},
					"body":         &graphql.InputObjectFieldConfig{Type: graphql.NewNonNull(graphql.String)},
					"thumbnailURL": &graphql.InputObjectFieldConfig{Type: graphql.String},
					"tagIDList":    &graphql.InputObjectFieldConfig{Type: graphql.NewList(graphql.NewNonNull(graphql.Int))},
				},
			}),
		},
	},
	Resolve: func(p graphql.ResolveParams) (interface{}, error) {
		// TODO - Authentication

		input := p.Args["input"].(map[string]interface{})

		post := Post{
			Title:       input["title"].(string),
			Description: input["description"].(string),
			Body:        input["body"].(string),
		}
		if t := input["thumbnailURL"]; t != nil {
			post.ThumbnailURL = t.(string)
		}
		errs := db.Save(&post).GetErrors()
		if len(errs) > 0 {
			return nil, ErrInternalServer
		}

		if tagIDList := input["tagIDList"]; tagIDList != nil {
			for _, id := range tagIDList.([]interface{}) {
				var tag PostTag
				db.Where(&PostTag{ID: id.(int)}).First(&tag)
				if tag.ID == 0 {
					continue
				}
				db.Save(&PostTagRelation{PostID: post.ID, TagID: tag.ID})
			}
		}
		return &post, nil
	},
}

var CreatePostTagMutation = &graphql.Field{
	Type: graphql.NewNonNull(PostTagType),
	Args: graphql.FieldConfigArgument{
		"input": &graphql.ArgumentConfig{
			Type: graphql.NewInputObject(graphql.InputObjectConfig{
				Name: "CreatePostTagInput",
				Fields: graphql.InputObjectConfigFieldMap{
					"name": &graphql.InputObjectFieldConfig{Type: graphql.NewNonNull(graphql.String)},
				},
			}),
		},
	},
	Resolve: func(p graphql.ResolveParams) (interface{}, error) {
		// TODO - Authentication

		tagName := p.Args["input"].(map[string]interface{})["name"].(string)

		var tag PostTag
		db.Where(&PostTag{Name: tagName}).First(&tag)
		if tag.Name == tagName {
			return nil, ErrPostTagDuplicated
		}

		tag = PostTag{Name: tagName}
		db.Save(&tag)
		return &tag, nil
	},
}
