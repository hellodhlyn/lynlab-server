package main

import (
	"fmt"

	"github.com/graphql-go/graphql"
	. "github.com/onsi/ginkgo"
	. "github.com/onsi/gomega"
)

func testMutation(mutationName, mutation string, args ...interface{}) (data map[string]interface{}) {
	result := graphql.Do(graphql.Params{
		Schema:        schema,
		RequestString: fmt.Sprintf(mutation, args...),
		Context:       mockContext,
	})

	if result.HasErrors() {
		fmt.Println(result.Errors)
		Fail("Failed to execute mutation.")
	}

	mutationData := result.Data.(map[string]interface{})[mutationName]
	if mutationData == nil {
		return nil
	}
	return mutationData.(map[string]interface{})
}

var _ = Describe("Mutation", func() {
	Describe("createPost", func() {
		testTitle := "Awesome post 😎"
		testBody := "This is my awesome post."
		testDescription := "This is my awesome description."

		It("create new post should success", func() {
			data := testMutation("createPost", `
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
			Expect(post.Title).To(Equal(testTitle))
			Expect(data["title"].(string)).To(Equal(testTitle))
			Expect(post.Description).To(Equal(testDescription))
			Expect(data["description"].(string)).To(Equal(testDescription))
		})

		It("create new post with tags should success", func() {
			tag1 := PostTag{Name: "my_tag_1"}
			tag2 := PostTag{Name: "my_tag_2"}
			db.Save(&tag1)
			db.Save(&tag2)

			data := testMutation("createPost", `
			mutation {
				createPost(input: {
					title: "%s"
					body: "%s"
					description: "%s"
					tagNameList: ["%s", "%s"]
				}) {
					id
				}
			}`, testTitle, testBody, testDescription, tag1.Name, tag2.Name)

			var rels []PostTagRelation
			db.Where(&PostTagRelation{PostID: data["id"].(int)}).Find(&rels)
			Expect(len(rels)).To(Equal(2))
		})
	})

	Describe("updatePost", func() {
		It("Update post should success", func() {
			testTitle := "Awesome updated post 😎"
			testBody := "This is my awesome updated post."
			testDescription := "This is my awesome updated description."

			var post Post
			db.First(&post)

			testMutation("updatePost", `
			mutation {
				updatePost(id: %d, input: {
					title: "%s"
					body: "%s"
					description: "%s"
				}) {
					id
				}
			}`, post.ID, testTitle, testBody, testDescription)

			db.Where(&Post{ID: post.ID}).First(&post)
			Expect(post.Title).To(Equal(testTitle))
			Expect(post.Body).To(Equal(testBody))
			Expect(post.Description).To(Equal(testDescription))
		})
	})

	Describe("createSnippet", func() {
		testTitle := "Awesome snippet 😎"
		testBody := "This is my awesome snippet."

		It("create new snippet should success", func() {
			data := testMutation("createSnippet", `
			mutation {
				createSnippet(input: {
					title: "%s"
					body: "%s"
					isPublic: true
				}) {
					id
					title
					body
				}
			}`, testTitle, testBody)

			var snippet Snippet
			db.Where(&Snippet{ID: data["id"].(int)}).First(&snippet)
			Expect(snippet.Title).To(Equal(testTitle))
			Expect(data["title"].(string)).To(Equal(testTitle))
		})
	})

	Describe("updateSnippet", func() {
		It("Update snippet should success", func() {
			testBody := "This is my awesome updated snippet."

			var snippet Snippet
			db.First(&snippet)

			testMutation("updateSnippet", `
			mutation {
				updateSnippet(id: %d, input: {
					body: "%s"
				}) {
					id
				}
			}`, snippet.ID, testBody)

			db.Where(&Snippet{ID: snippet.ID}).First(&snippet)
			Expect(snippet.Body).To(Equal(testBody))
		})
	})
})
