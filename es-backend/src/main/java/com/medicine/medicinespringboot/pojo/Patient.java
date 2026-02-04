package com.medicine.medicinespringboot.pojo;

import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.Pattern;
import lombok.Data;

import java.time.LocalDate;


@Data
public class Patient {
    private Integer id; //患者id
    @NotEmpty
    private String name;    //患者姓名
    @NotEmpty
    private String age; //患者年龄
    @NotEmpty
    private String male;    //患者性别
    @NotEmpty
    @Pattern(regexp = "^1[3-9]\\d{9}$")
    private String phone;   //手机号码
    @NotEmpty
    private String address; //家庭住址
    private String doctorId;    //主治医生
    private String departmentId;    //病房号
    private String diagnosis;   //诊断(主要病症)
    private String text;              //病情(详细病情)
    private LocalDate createTime;   //创建时间
    private LocalDate updateTime;   //更新时间
}
