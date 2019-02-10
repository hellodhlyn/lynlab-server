package main

import (
	"math"
	"strconv"
	"time"

	"github.com/graphql-go/graphql"
)

var PostQuery = &graphql.Field{
	Type: PostType,
	Args: graphql.FieldConfigArgument{
		"id": &graphql.ArgumentConfig{Type: graphql.NewNonNull(graphql.Int)},
	},
	Resolve: func(p graphql.ResolveParams) (interface{}, error) {
		id := p.Args["id"].(int)
		var post Post
		db.Where(id).First(&post)

		if post.ID != id || !post.IsPublic {
			return nil, nil
		}

		cacheKey := "post.readcount." + strconv.Itoa(id) + "." + p.Context.Value(ctxClientIP).(string)
		if _, ok := cache.Get(cacheKey); !ok {
			post.ReadCount = post.ReadCount + 1
			db.Save(&post)

			cache.Set(cacheKey, true, 24*time.Hour)
		}

		return &post, nil
	},
}

var PostListQuery = &graphql.Field{
	Type: pageTypeOf(PostType),
	Args: graphql.FieldConfigArgument{
		"page": &pageArguments,
	},
	Resolve: func(p graphql.ResolveParams) (interface{}, error) {
		pageArgs := p.Args["page"].(map[string]interface{})
		var items []Post

		query := db
		if before, ok := pageArgs["before"].(int); ok {
			query = query.Where("id < ?", before)
		}
		query = query.Where(&Post{IsPublic: true})

		switch pageArgs["sortDirection"].(string) {
		case "ASC":
			query = query.Order("id asc")
		default:
			query = query.Order("id desc")
		}

		errors := query.Limit(pageArgs["count"].(int)).Find(&items).GetErrors()
		if len(errors) > 0 {
			return nil, errors[0]
		}

		maxID := math.MinInt32
		minID := math.MaxInt32
		for _, p := range items {
			if maxID < p.ID {
				maxID = p.ID
			}
			if minID > p.ID {
				minID = p.ID
			}
		}

		var beforeCount int
		var nextCount int
		switch pageArgs["sortDirection"].(string) {
		case "ASC":
			db.Model(&Post{}).Where("id < ?", minID).Where(&Post{IsPublic: true}).Count(&beforeCount)
			db.Model(&Post{}).Where("id > ?", maxID).Where(&Post{IsPublic: true}).Count(&nextCount)
		case "DESC":
			db.Model(&Post{}).Where("id < ?", minID).Where(&Post{IsPublic: true}).Count(&nextCount)
			db.Model(&Post{}).Where("id > ?", maxID).Where(&Post{IsPublic: true}).Count(&beforeCount)
		}

		return &PostPage{
			Items: items,
			PageInfo: pageInfo{
				HasBefore: beforeCount > 0,
				HasNext:   nextCount > 0,
			},
		}, nil
	},
}

var SnippetQuery = &graphql.Field{
	Type: SnippetType,
	Args: graphql.FieldConfigArgument{
		"id":    &graphql.ArgumentConfig{Type: graphql.Int},
		"title": &graphql.ArgumentConfig{Type: graphql.String},
	},
	Resolve: func(p graphql.ResolveParams) (interface{}, error) {
		var snippet Snippet

		if id, ok := p.Args["id"].(int); ok {
			db.Where(id).First(&snippet)
		} else if title, ok := p.Args["title"].(string); ok {
			db.Where(&Snippet{Title: title}).First(&snippet)
		} else {
			return nil, nil
		}

		if snippet.ID == 0 {
			return nil, nil
		}
		return &snippet, nil
	},
}

var SnippetListQuery = &graphql.Field{
	Type: pageTypeOf(SnippetType),
	Args: graphql.FieldConfigArgument{
		"page": &pageArguments,
	},
	Resolve: func(p graphql.ResolveParams) (interface{}, error) {
		pageArgs := p.Args["page"].(map[string]interface{})
		var items []Snippet

		query := db
		if before, ok := pageArgs["before"].(int); ok {
			query = query.Where("id < ?", before)
		}

		switch pageArgs["sortDirection"].(string) {
		case "ASC":
			query = query.Order("id asc")
		default:
			query = query.Order("id desc")
		}

		errors := query.Limit(pageArgs["count"].(int)).Find(&items).GetErrors()
		if len(errors) > 0 {
			return nil, errors[0]
		}

		maxID := math.MinInt32
		minID := math.MaxInt32
		for _, p := range items {
			if maxID < p.ID {
				maxID = p.ID
			}
			if minID > p.ID {
				minID = p.ID
			}
		}

		var beforeCount int
		var nextCount int
		switch pageArgs["sortDirection"].(string) {
		case "ASC":
			db.Model(&Snippet{}).Where("id < ?", minID).Count(&beforeCount)
			db.Model(&Snippet{}).Where("id > ?", maxID).Count(&nextCount)
		case "DESC":
			db.Model(&Snippet{}).Where("id < ?", minID).Count(&nextCount)
			db.Model(&Snippet{}).Where("id > ?", maxID).Count(&beforeCount)
		}

		return &SnippetPage{
			Items: items,
			PageInfo: pageInfo{
				HasBefore: beforeCount > 0,
				HasNext:   nextCount > 0,
			},
		}, nil
	},
}
