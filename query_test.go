package main

import (
	"context"
	"fmt"

	"github.com/google/uuid"
	"github.com/graphql-go/graphql"
	. "github.com/onsi/ginkgo"
	. "github.com/onsi/gomega"
)

func testQuery(ctx context.Context, queryName, query string, args ...interface{}) (data map[string]interface{}) {
	result := graphql.Do(graphql.Params{
		Schema:        schema,
		RequestString: fmt.Sprintf(query, args...),
		Context:       ctx,
	})

	if result.HasErrors() {
		fmt.Println(result.Errors)
		Fail("Failed to execute query.")
	}

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
				IsPublic:    true,
			}
			db.Save(&post)
		})

		AfterEach(func() {
			db.Delete(&Post{})
		})

		It("get a post should success", func() {
			data := testQuery(mockContext, "post", `
			query {
				post(id: %d) {
					title
					body
					description
				}
			}`, post.ID)

			Expect(data).NotTo(BeNil())
			Expect(data["title"].(string)).To(Equal(testTitle))
			Expect(data["body"].(string)).To(Equal(testBody))
			Expect(data["description"].(string)).To(Equal(testDescription))
		})

		Context("get a private post", func() {
			BeforeEach(func() {
				post.IsPublic = false
				db.Save(&post)
			})

			It("without permission should return nil", func() {
				data := testQuery(mockContext, "post", `
				query {
					post(id: %d) {
						title
						body
						description
					}
				}`, post.ID)

				Expect(data).To(BeNil())
			})

			It("with permission should success", func() {
				data := testQuery(mockAuthContext, "post", `
				query {
					post(id: %d) {
						title
						body
						description
					}
				}`, post.ID)

				Expect(data).NotTo(BeNil())
			})
		})

		It("get a post with invalid id should fail", func() {
			data := testQuery(mockContext, "post", `
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

		BeforeEach(func() {
			db.Delete(&Post{})

			for range []int{0, 1, 2, 3, 4} {
				publicPost := Post{
					Title:       testTitle,
					Body:        testBody,
					Description: testDescription,
					IsPublic:    true,
				}
				privatePost := Post{
					Title:       testTitle,
					Body:        testBody,
					Description: testDescription,
					IsPublic:    false,
				}

				db.Save(&publicPost)
				db.Save(&privatePost)
			}
		})

		Context("get posts", func() {
			It("should success for admin user", func() {
				data := testQuery(mockAuthContext, "postList", `
				query {
					postList(page: {count: 10}) {
						items { id }
					}
				}`)

				Expect(len(data["items"].([]interface{}))).To(Equal(10))
			})

			It("should return only public posts for non-admin user", func() {
				data := testQuery(mockContext, "postList", `
				query {
					postList(page: {count: 10}) {
						items { id }
					}
				}`)

				Expect(len(data["items"].([]interface{}))).To(Equal(5))
			})
		})

	})
})

var _ = Describe("Snippet", func() {
	Describe("snippet", func() {
		var snippet Snippet

		BeforeEach(func() {
			id, _ := uuid.NewUUID()
			snippet = Snippet{
				Title: id.String(),
				Body:  "This is my awesome snippet.",
			}
			db.Save(&snippet)
		})

		It("get a snippet by id should success", func() {
			data := testQuery(mockContext, "snippet", `
			query {
				snippet(id: %d) {
					title
					body
				}
			}`, snippet.ID)

			Expect(data["title"].(string)).To(Equal(snippet.Title))
			Expect(data["body"].(string)).To(Equal(snippet.Body))
		})

		It("get a snippet by title should success", func() {
			data := testQuery(mockContext, "snippet", `
			query {
				snippet(title: "%s") {
					title
					body
				}
			}`, snippet.Title)

			Expect(data["title"].(string)).To(Equal(snippet.Title))
			Expect(data["body"].(string)).To(Equal(snippet.Body))
		})

		It("get a snippet with invalid id should return nil", func() {
			data := testQuery(mockContext, "snippet", `
			query {
				snippet(id : %d) {
					title
				}
			}`, -1)

			Expect(data).To(BeNil())
		})

		It("get a snippet with invalid title should  return nil", func() {
			data := testQuery(mockContext, "snippet", `
			query {
				snippet(title: "%s") {
					title
				}
			}`, snippet.Title+" invalid")

			Expect(data).To(BeNil())
		})
	})

	Describe("snippetList", func() {
		var snippets []Snippet

		BeforeEach(func() {
			for range []int{0, 1, 2, 3, 4} {
				id, _ := uuid.NewUUID()
				p := Snippet{
					Title: id.String(),
					Body:  "This is my awesome snippet.",
				}

				db.Save(&p)
				snippets = append(snippets, p)
			}
		})

		It("get snippet list should success", func() {
			data := testQuery(mockContext, "snippetList", `
			query {
				snippetList(page: {count: 10}) {
					items { title }
					pageInfo { hasNext, hasBefore }
				}
			}`)

			Expect(len(data["items"].([]interface{})) > 0).To(BeTrue())
		})
	})
})
