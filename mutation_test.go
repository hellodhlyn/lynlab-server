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
	})

	Expect(result.HasErrors()).To(BeFalse())

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
					tagIDList: [%d, %d]
				}) {
					id
				}
			}`, testTitle, testBody, testDescription, tag1.ID, tag2.ID)

			var rels []PostTagRelation
			db.Where(&PostTagRelation{PostID: data["id"].(int)}).Find(&rels)
			Expect(len(rels)).To(Equal(2))
		})
	})

	Describe("createPostTag", func() {
		It("create post tag should success", func() {
			testMutation("createPostTag", `
			mutation {
				createPostTag(input: { name: "awesome" }) {
					name
				}
			}`)

			var tag PostTag
			db.Where(&PostTag{Name: "awesome"}).First(&tag)
			Expect(tag.Name).To(Equal("awesome"))
		})
	})
})
