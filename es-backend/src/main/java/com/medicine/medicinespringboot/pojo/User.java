package com.medicine.medicinespringboot.pojo;

import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.Data;

import java.time.LocalDateTime;


@Data
public class User {
    private String id;  //ID
    private String username;   //用户名
    private String name;    //姓名
    private String password;    //密码
    private Integer userStatus; //状态
    private String phone;   //手机号
    private String email;    //邮箱
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss", timezone = "GMT+8")
    private LocalDateTime createTime;//创建时间
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss", timezone = "GMT+8")
    private LocalDateTime updateTime;//更新时间
}
