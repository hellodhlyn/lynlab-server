package main

import (
	"time"

	"github.com/graphql-go/graphql"
)

// User is a model stands for each logged-in user.
// Authentication mehtod uses LYnLab Auth service (https://auth.lynlab.co.kr).
type User struct {
	ID        string `gorm:"type:varchar(40)"`
	Username  string `gorm:"type:varchar(255)"`
	IsAdmin   bool   `gorm:"default:false"`
	CreatedAt time.Time
	UpdatedAt time.Time
}

// Post is a model for blog post.
type Post struct {
	ID           int
	Title        string `gorm:"type:varchar(255);not null"`
	Description  string `gorm:"type:text;not null"`
	Body         string `gorm:"type:text;not null"`
	ThumbnailURL string `gorm:"type:varchar(255);nullable"`
	ReadCount    int    `gorm:"default:0"`
	IsPublic     bool   `gorm:"default:false"`
	CreatedAt    time.Time
	UpdatedAt    time.Time
}

type PostPage struct {
	Items    []*Post
	PageInfo pageInfo
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
		"isPublic":  &graphql.Field{Type: graphql.NewNonNull(graphql.Boolean)},
		"createdAt": &graphql.Field{Type: graphql.NewNonNull(graphql.DateTime)},
		"updatedAt": &graphql.Field{Type: graphql.NewNonNull(graphql.DateTime)},
	},
})

// PostTag is a model for tag of the posts.
type PostTag struct {
	ID        int
	Name      string `gorm:"type:varchar(255);not null"`
	CreatedAt time.Time
	UpdatedAt time.Time
}

// PostTagRelation is a relation table between Post and PostTag models.
type PostTagRelation struct {
	PostID int `gorm:"not null"`
	TagID  int `gorm:"not null"`
}

// PostTagType represents a GraphQL object for tags of blog posts.
var PostTagType = graphql.NewObject(graphql.ObjectConfig{
	Name: "PostTag",
	Fields: graphql.Fields{
		"id":   &graphql.Field{Type: graphql.NewNonNull(graphql.Int)},
		"name": &graphql.Field{Type: graphql.NewNonNull(graphql.String)},
	},
})

// Snippet is a model for text storage system, like a GitHub Gist.
type Snippet struct {
	ID         int
	AuthorUUID string `gorm:"type:varchar(40)"`
	Title      string `gorm:"type:varchar(255);unique_index;not null"`
	Body       string `gorm:"type:text;not null"`
	IsPublic   bool   `gorm:"default:false"`
	CreatedAt  time.Time
	UpdatedAt  time.Time
}

type SnippetPage struct {
	Items    []*Snippet
	PageInfo pageInfo
}

// SnippetType represents a GraphQL object for snippet.
var SnippetType = graphql.NewObject(graphql.ObjectConfig{
	Name: "Snippet",
	Fields: graphql.Fields{
		"id":        &graphql.Field{Type: graphql.NewNonNull(graphql.Int)},
		"title":     &graphql.Field{Type: graphql.NewNonNull(graphql.String)},
		"body":      &graphql.Field{Type: graphql.NewNonNull(graphql.String)},
		"isPublic":  &graphql.Field{Type: graphql.NewNonNull(graphql.Boolean)},
		"createdAt": &graphql.Field{Type: graphql.NewNonNull(graphql.DateTime)},
		"updatedAt": &graphql.Field{Type: graphql.NewNonNull(graphql.DateTime)},
	},
})

func migrateModels() {
	db.AutoMigrate(
		Post{},
		PostTag{},
		PostTagRelation{},
		Snippet{},
		User{},
	)
}

func cleanModels() {
	db.DropTable(
		Post{},
		PostTag{},
		PostTagRelation{},
		Snippet{},
		User{},
	)
}

func init() {
	migrateModels()
}
