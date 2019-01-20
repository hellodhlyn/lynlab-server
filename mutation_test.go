package main

import (
	"fmt"
	"testing"

	"github.com/graphql-go/graphql"
)

func testMutation(t *testing.T, mutationName, mutation string, args ...interface{}) (data map[string]interface{}) {
	result := graphql.Do(graphql.Params{
		Schema:        schema,
		RequestString: fmt.Sprintf(mutation, args...),
	})

	if result.HasErrors() {
		fmt.Printf("%s mutation return error(s): %v\n", mutationName, result.Errors)
		t.FailNow()
		return nil
	}
	return result.Data.(map[string]interface{})[mutationName].(map[string]interface{})
}

func TestCreatePostMutation(t *testing.T) {
	testTitle := "Awesome post 😎"
	testBody := "This is my awesome post."
	testDescription := "This is my awesome description."

	// Create new post
	data := testMutation(t, "createPost", `
	mutation {
		createPost(input: {
			title: "%s"
			body: "%s"
			description: "%s"
		}) {
			id
			title
			body
			description
		}
	}`, testTitle, testBody, testDescription)

	var post Post
	db.Where(&Post{ID: data["id"].(int)}).First(&post)
	if post.Title != testTitle || data["title"].(string) != testTitle ||
		post.Body != testBody || data["body"].(string) != testBody ||
		post.Description != testDescription || data["description"].(string) != testDescription {
		fmt.Printf("createPost failed: %v\n", post)
		t.FailNow()
		return
	}

	// Create new post with tags
	db.Save(&PostTag{Name: "my_tag_1"})
	db.Save(&PostTag{Name: "my_tag_2"})
	var tag1 PostTag
	var tag2 PostTag
	db.Where(&PostTag{Name: "my_tag_1"}).First(&tag1)
	db.Where(&PostTag{Name: "my_tag_2"}).First(&tag2)

	data = testMutation(t, "createPost", `
	mutation {
		createPost(input: {
			title: "%s"
			body: "%s"
			description: "%s"
			tagIDList: [%d, %d]
		}) {
			id
		}
	}`, testTitle, testBody, testDescription, tag1.ID, tag2.ID)

	var rels []PostTagRelation
	db.Where(&PostTagRelation{PostID: data["id"].(int)}).Find(&rels)
	if len(rels) != 2 {
		fmt.Printf("createPost failed\n")
		t.FailNow()
		return
	}
}

func TestCreatePostTagMutation(t *testing.T) {
	testMutation(t, "createPostTag", `
	mutation {
		createPostTag(input: { name: "awesome" }) {
			name
		}
	}`)

	var tag PostTag
	db.Where(&PostTag{Name: "awesome"}).First(&tag)
	if tag.Name != "awesome" {
		fmt.Printf("createPostTag failed\n")
		t.FailNow()
		return
	}
}
