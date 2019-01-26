package main

import (
	"bytes"
	"net/http"

	"github.com/graphql-go/graphql"
	"github.com/labstack/echo"
	"github.com/labstack/echo/middleware"
)

var schema graphql.Schema

func init() {
	schema, _ = graphql.NewSchema(graphql.SchemaConfig{
		Query: graphql.NewObject(graphql.ObjectConfig{
			Name: "RootQuery",
			Fields: graphql.Fields{
				"post":     PostQuery,
				"postList": PostListQuery,
			},
		}),
		Mutation: graphql.NewObject(graphql.ObjectConfig{
			Name: "RootMutation",
			Fields: graphql.Fields{
				"createPost":    CreatePostMutation,
				"createPostTag": CreatePostTagMutation,
			},
		}),
	})
}

func main() {
	e := echo.New()
	e.Any("/graphql", func(c echo.Context) error {
		var req string
		if c.Request().Method == "GET" {
			req = c.QueryParam("query")
		} else if c.Request().Method == "POST" {
			buf := new(bytes.Buffer)
			buf.ReadFrom(c.Request().Body)
			req = buf.String()
		}

		// Run query and return the result.
		result := graphql.Do(graphql.Params{
			Schema:        schema,
			RequestString: req,
		})

		return c.JSON(http.StatusOK, result)
	})

	e.Use(middleware.GzipWithConfig(middleware.GzipConfig{Level: 5}))
	e.Logger.Fatal(e.Start(":1323"))
}
