package main

import "testing"

func cleanModels() {
	db.DropTable(
		Post{},
		PostTag{},
		PostTagRelation{},
	)
}

func TestMain(m *testing.M) {
	cleanModels()
	migrateModels()

	m.Run()

	defer cleanModels()
}
