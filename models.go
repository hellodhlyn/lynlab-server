package main

import (
	"time"

	"github.com/graphql-go/graphql"
)

// Post is a model for blog post.
type Post struct {
	ID           int
	Title        string `gorm:"type:varchar(255)"`
	Description  string
	Body         string
	ThumbnailURL string `gorm:"type:varchar(255);NULLABLE"`
	ReadCount    int
	CreatedAt    time.Time
	UpdatedAt    time.Time
}

// PostTag is a model for tag of the posts.
type PostTag struct {
	ID        int
	Name      string
	CreatedAt time.Time
	UpdatedAt time.Time
}

// PostTagRelation is a relation table between Post and PostTag models.
type PostTagRelation struct {
	PostID int
	TagID  int
}

// PostType represents a GraphQL object for blog posts.
var PostType = graphql.NewObject(graphql.ObjectConfig{
	Name: "Post",
	Fields: graphql.Fields{
		"id":           &graphql.Field{Type: graphql.NewNonNull(graphql.Int)},
		"title":        &graphql.Field{Type: graphql.NewNonNull(graphql.String)},
		"description":  &graphql.Field{Type: graphql.NewNonNull(graphql.String)},
		"body":         &graphql.Field{Type: graphql.NewNonNull(graphql.String)},
		"thumbnailURL": &graphql.Field{Type: graphql.String},
		"tagList": &graphql.Field{
			Type: graphql.NewNonNull(graphql.NewList(graphql.NewNonNull(PostTagType))),
			Resolve: func(p graphql.ResolveParams) (interface{}, error) {
				var rels []PostTagRelation
				db.Where(&PostTagRelation{PostID: p.Source.(*Post).ID}).Find(&rels)
				if len(rels) == 0 {
					return rels, nil
				}

				var tagIDs []int
				for _, r := range rels {
					tagIDs = append(tagIDs, r.TagID)
				}

				var tags []PostTag
				db.Where(tagIDs).Find(&tags)
				return tags, nil
			},
		},
		"readCount": &graphql.Field{Type: graphql.NewNonNull(graphql.Int)},
		"createdAt": &graphql.Field{Type: graphql.NewNonNull(graphql.DateTime)},
		"updatedAt": &graphql.Field{Type: graphql.NewNonNull(graphql.DateTime)},
	},
})

// PostTagType represents a GraphQL object for tags of blog posts.
var PostTagType = graphql.NewObject(graphql.ObjectConfig{
	Name: "PostTag",
	Fields: graphql.Fields{
		"id":   &graphql.Field{Type: graphql.NewNonNull(graphql.Int)},
		"name": &graphql.Field{Type: graphql.NewNonNull(graphql.String)},
	},
})

func migrateModels() {
	db.AutoMigrate(
		Post{},
		PostTag{},
		PostTagRelation{},
	)
}

func init() {
	migrateModels()
}
