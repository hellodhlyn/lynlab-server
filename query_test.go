package main

import (
	"fmt"
	"testing"

	"github.com/graphql-go/graphql"
)

func testQuery(t *testing.T, queryName, query string, args ...interface{}) (data map[string]interface{}) {
	result := graphql.Do(graphql.Params{
		Schema:        schema,
		RequestString: fmt.Sprintf(query, args...),
	})

	if result.HasErrors() {
		fmt.Printf("%s query return error(s): %v\n", queryName, result.Errors)
		t.FailNow()
		return nil
	}

	queryData := result.Data.(map[string]interface{})[queryName]
	if queryData == nil {
		return nil
	}
	return queryData.(map[string]interface{})
}

func TestPostQuery(t *testing.T) {
	testTitle := "Awesome post 😎"
	testBody := "This is my awesome post."
	testDescription := "This is my awesome description."

	post := Post{
		Title:       testTitle,
		Body:        testBody,
		Description: testDescription,
	}
	db.Save(&post)

	// Get a post
	data := testQuery(t, "post", `
	query {
		post(id: %d) {
			title
			body
			description
		}
	}`, post.ID)

	if data["title"].(string) != testTitle ||
		data["body"].(string) != testBody ||
		data["description"].(string) != testDescription {
		fmt.Printf("post query failed: %v\n", data)
		t.Fail()
		return
	}

	// Try to get a post with invalid id
	data = testQuery(t, "post", `
	query {
		post(id : %d) {
			title
		}
	}
	`, -1)

	if data != nil {
		fmt.Printf("post query failed: %v\n", data)
		t.Fail()
		return
	}
}

func TestPostList(t *testing.T) {
	testTitle := "Awesome post 😎"
	testBody := "This is my awesome post."
	testDescription := "This is my awesome description."

	var posts []Post
	for range []int{0, 1, 2, 3, 4} {
		p := Post{
			Title:       testTitle,
			Body:        testBody,
			Description: testDescription,
		}

		db.Save(&p)
		posts = append(posts, p)
	}

	// Get posts
	data := testQuery(t, "postList", `
	query {
		postList(page: {count: 10}) {
			items { title }
			pageInfo { hasNext, hasBefore }
		}
	}`)
	if len(data["items"].([]interface{})) == 0 {
		fmt.Printf("postList query failed: %v\n", data)
		t.Fail()
		return
	}
}
