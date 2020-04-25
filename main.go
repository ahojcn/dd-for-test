package main

import (
	"github.com/gin-gonic/gin"
	"github.com/smokezl/govalidators"
	"log"
)

func main() {
	router := gin.Default()

	router.POST("/DD", DD)

	err := router.Run(":8383")
	if err != nil {
		log.Fatalf("error: %v", err)
	}
}

// 用户基本信息
type PersonalInfo struct {
	Name   string `json:"Name" validate:"string=2,20"`             // 姓名: 最短2位，最长20位
	Height int    `json:"Height" validate:"integer=50,300"`        // 身高: [50, 300]cm
	Weight int    `json:"Weight" validate:"integer=20,1000"`       // 体重: [20, 1k] kg
	Gender string `json:"Gender" validate:"in=male,female,secret"` // 性别: 男/女/保密
	Age    int    `json:"Age" validate:"integer=6,110"`            // 年龄: [6, 110]岁
	Email  string `json:"Email" validate:"email"`                  // 邮箱
}

// 校验用户信息
func (info *PersonalInfo) Check() error {
	validator := govalidators.New()
	return validator.LazyValidate(info)
}

// 响应数据
type RespData struct {
	Status  int         `json:"status"`
	Message string      `json:"message"`
	Data    interface{} `json:"data"`
}

// POST: /DD
func DD(ctx *gin.Context) {
	var respData RespData
	var info PersonalInfo
	err := ctx.ShouldBindJSON(&info)
	if err == nil {
		e := info.Check() // 参数校验！
		if e != nil {
			respData.Status = -1
			respData.Message = e.Error()
		} else {
			respData.Status = 0
			respData.Message = "ok"
		}
		respData.Data = info
	} else {
		respData.Status = -2
		respData.Message = "params error"
		respData.Data = nil
	}

	ctx.JSON(200, respData)
}
