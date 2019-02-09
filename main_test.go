package main

import (
	"testing"

	. "github.com/onsi/ginkgo"
	. "github.com/onsi/gomega"
)

func cleanModels() {
	db.DropTable(
		Post{},
		PostTag{},
		PostTagRelation{},
		Snippet{},
	)
}

func TestMain(m *testing.M) {
	cleanModels()
	migrateModels()
	defer cleanModels()

	m.Run()
}

func TestAll(t *testing.T) {
	RegisterFailHandler(Fail)
	RunSpecs(t, "All Suite")
}
