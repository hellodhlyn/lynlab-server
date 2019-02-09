package main

import (
	"fmt"

	"github.com/graphql-go/graphql"
	. "github.com/onsi/ginkgo"
	. "github.com/onsi/gomega"
)

func testQuery(queryName, query string, args ...interface{}) (data map[string]interface{}) {
	result := graphql.Do(graphql.Params{
		Schema:        schema,
		RequestString: fmt.Sprintf(query, args...),
	})

	Expect(result.HasErrors()).To(BeFalse())

	queryData := result.Data.(map[string]interface{})[queryName]
	if queryData == nil {
		return nil
	}
	return queryData.(map[string]interface{})
}

var _ = Describe("Query", func() {
	Describe("post", func() {
		testTitle := "Awesome post 😎"
		testBody := "This is my awesome post."
		testDescription := "This is my awesome description."

		var post Post

		BeforeEach(func() {
			post = Post{
				Title:       testTitle,
				Body:        testBody,
				Description: testDescription,
			}
			db.Save(&post)
		})

		It("get a post should success", func() {
			data := testQuery("post", `
			query {
				post(id: %d) {
					title
					body
					description
				}
			}`, post.ID)

			Expect(data["title"].(string)).To(Equal(testTitle))
			Expect(data["body"].(string)).To(Equal(testBody))
			Expect(data["description"].(string)).To(Equal(testDescription))
		})

		It("get a post with invalid id should fail", func() {
			data := testQuery("post", `
			query {
				post(id : %d) {
					title
				}
			}
			`, -1)

			Expect(data).To(BeNil())
		})
	})

	Describe("postList", func() {
		testTitle := "Awesome post 😎"
		testBody := "This is my awesome post."
		testDescription := "This is my awesome description."

		var posts []Post

		BeforeEach(func() {
			for range []int{0, 1, 2, 3, 4} {
				p := Post{
					Title:       testTitle,
					Body:        testBody,
					Description: testDescription,
				}

				db.Save(&p)
				posts = append(posts, p)
			}
		})

		It("get post list should success", func() {
			data := testQuery("postList", `
			query {
				postList(page: {count: 10}) {
					items { title }
					pageInfo { hasNext, hasBefore }
				}
			}`)

			Expect(len(data["items"].([]interface{})) > 0).To(BeTrue())
		})
	})
})
