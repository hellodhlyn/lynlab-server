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
					"tagNameList":  &graphql.InputObjectFieldConfig{Type: graphql.NewList(graphql.NewNonNull(graphql.String))},
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

		if tagNameList := input["tagNameList"]; tagNameList != nil {
			for _, name := range tagNameList.([]interface{}) {
				var tag PostTag
				db.Where(&PostTag{Name: name.(string)}).FirstOrCreate(&tag)
				db.Save(&PostTagRelation{PostID: post.ID, TagID: tag.ID})
			}
		}
		return &post, nil
	},
}

var UpdatePostMutation = &graphql.Field{
	Type: graphql.NewNonNull(PostType),
	Args: graphql.FieldConfigArgument{
		"id": &graphql.ArgumentConfig{Type: graphql.NewNonNull(graphql.Int)},
		"input": &graphql.ArgumentConfig{
			Type: graphql.NewInputObject(graphql.InputObjectConfig{
				Name: "UpdatePostInput",
				Fields: graphql.InputObjectConfigFieldMap{
					"title":        &graphql.InputObjectFieldConfig{Type: graphql.String},
					"description":  &graphql.InputObjectFieldConfig{Type: graphql.String},
					"body":         &graphql.InputObjectFieldConfig{Type: graphql.String},
					"thumbnailURL": &graphql.InputObjectFieldConfig{Type: graphql.String},
					"tagNameList":  &graphql.InputObjectFieldConfig{Type: graphql.NewList(graphql.NewNonNull(graphql.String))},
				},
			}),
		},
	},
	Resolve: func(p graphql.ResolveParams) (interface{}, error) {
		// TODO - Authentication

		postID := p.Args["id"].(int)
		var post Post
		db.Where(&Post{ID: postID}).First(&post)
		if post.ID != postID {
			return nil, ErrBadRequest
		}

		input := p.Args["input"].(map[string]interface{})
		if t := input["title"]; t != nil {
			post.Title = t.(string)
		}
		if d := input["description"]; d != nil {
			post.Description = d.(string)
		}
		if b := input["body"]; b != nil {
			post.Body = b.(string)
		}
		if t := input["thumbnailURL"]; t != nil {
			post.ThumbnailURL = t.(string)
		}
		errs := db.Save(&post).GetErrors()
		if len(errs) > 0 {
			return nil, ErrInternalServer
		}

		if tagNameList := input["tagNameList"]; tagNameList != nil {
			db.Where(&PostTagRelation{PostID: post.ID}).Delete(&PostTagRelation{})

			for _, name := range tagNameList.([]interface{}) {
				var tag PostTag
				db.Where(&PostTag{Name: name.(string)}).FirstOrCreate(&tag)
				db.Save(&PostTagRelation{PostID: post.ID, TagID: tag.ID})
			}
		}
		return &post, nil
	},
}

var CreateSnippetMutation = &graphql.Field{
	Type: graphql.NewNonNull(SnippetType),
	Args: graphql.FieldConfigArgument{
		"input": &graphql.ArgumentConfig{
			Type: graphql.NewInputObject(graphql.InputObjectConfig{
				Name: "CreateSnippetInput",
				Fields: graphql.InputObjectConfigFieldMap{
					"title":    &graphql.InputObjectFieldConfig{Type: graphql.NewNonNull(graphql.String)},
					"body":     &graphql.InputObjectFieldConfig{Type: graphql.NewNonNull(graphql.String)},
					"isPublic": &graphql.InputObjectFieldConfig{Type: graphql.NewNonNull(graphql.Boolean)},
				},
			}),
		},
	},
	Resolve: func(p graphql.ResolveParams) (interface{}, error) {
		// TODO - Authentication

		input := p.Args["input"].(map[string]interface{})
		snippet := Snippet{
			Title:    input["title"].(string),
			Body:     input["body"].(string),
			IsPublic: input["isPublic"].(bool),
		}

		errs := db.Save(&snippet).GetErrors()
		if len(errs) > 0 {
			return nil, ErrInternalServer
		}
		return &snippet, nil
	},
}

var UpdateSnippetMutation = &graphql.Field{
	Type: graphql.NewNonNull(SnippetType),
	Args: graphql.FieldConfigArgument{
		"id": &graphql.ArgumentConfig{Type: graphql.NewNonNull(graphql.Int)},
		"input": &graphql.ArgumentConfig{
			Type: graphql.NewInputObject(graphql.InputObjectConfig{
				Name: "SnippetInput",
				Fields: graphql.InputObjectConfigFieldMap{
					"body": &graphql.InputObjectFieldConfig{Type: graphql.String},
				},
			}),
		},
	},
	Resolve: func(p graphql.ResolveParams) (interface{}, error) {
		// TODO - Authentication

		snippetID := p.Args["id"].(int)
		var snippet Snippet
		db.Where(snippetID).First(&snippet)
		if snippet.ID != snippetID {
			return nil, ErrBadRequest
		}

		input := p.Args["input"].(map[string]interface{})
		if b := input["body"]; b != nil {
			snippet.Body = b.(string)
		}

		errs := db.Save(&snippet).GetErrors()
		if len(errs) > 0 {
			return nil, ErrInternalServer
		}
		return &snippet, nil
	},
}
