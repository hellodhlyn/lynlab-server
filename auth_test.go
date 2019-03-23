package main

import (
	. "github.com/onsi/ginkgo"
	. "github.com/onsi/gomega"
)

var _ = Describe("Auth", func() {
	It("success", func() {
		res, err := Authenticate("Bearer valid_token")
		Expect(err).To(BeNil())
		Expect(res.UUID).To(Equal("00000000-0000-0000-0000-000000000000"))
		Expect(res.Email).To(Equal("test@email.com"))
		Expect(res.Username).To(Equal("TestUsername"))
	})

	It("failure", func() {
		_, err := Authenticate("Bearer invalid_token")
		Expect(err).To(Equal(ErrForbidden))
	})
})
