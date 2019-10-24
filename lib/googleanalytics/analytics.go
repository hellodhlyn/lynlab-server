package googleanalytics

import (
	"context"
	"encoding/base64"
	"fmt"
	"os"
	"strconv"

	"google.golang.org/api/analyticsreporting/v4"
	option "google.golang.org/api/option"
)

var service *analyticsreporting.Service

func GetPageView(pagePath string) (int, error) {
	req := analyticsreporting.GetReportsRequest{
		ReportRequests: []*analyticsreporting.ReportRequest{
			&analyticsreporting.ReportRequest{
				ViewId: os.Getenv("GOOGLE_ANALYTICS_VIEW_ID"),
				DateRanges: []*analyticsreporting.DateRange{
					&analyticsreporting.DateRange{StartDate: "2010-01-01", EndDate: "2099-12-31"},
				},
				Metrics: []*analyticsreporting.Metric{
					&analyticsreporting.Metric{Expression: "ga:pageviews"},
				},
				DimensionFilterClauses: []*analyticsreporting.DimensionFilterClause{
					&analyticsreporting.DimensionFilterClause{
						Filters: []*analyticsreporting.DimensionFilter{
							&analyticsreporting.DimensionFilter{
								Operator:      "EXACT",
								DimensionName: "ga:pagePath",
								Expressions:   []string{pagePath},
							},
						},
					},
				},
			},
		},
	}

	res, err := service.Reports.BatchGet(&req).Do()
	if err != nil {
		fmt.Println(err)
		return -1, err
	}

	if len(res.Reports) == 0 || len(res.Reports[0].Data.Rows) == 0 {
		return 0, nil
	}
	value, _ := strconv.Atoi(res.Reports[0].Data.Rows[0].Metrics[0].Values[0])
	return value, nil
}

func init() {
	credEncoded := os.Getenv("GOOGLE_SERVICE_ACCOUNTS")
	cred, err := base64.StdEncoding.DecodeString(credEncoded)
	if err != nil {
		panic(err)
	}

	ctx := context.Background()
	newService, err := analyticsreporting.NewService(ctx, option.WithCredentialsJSON(cred))
	if err != nil {
		panic(err)
	}
	service = newService
}
