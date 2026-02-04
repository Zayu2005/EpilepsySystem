package com.medicine.medicinespringboot.pojo;

import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.Data;

import java.time.LocalDateTime;
import java.util.List;



@Data
public class EegAnalysisResult {
    private Integer id;

    private String fileName;    //文件名
    private Long fileSize;  //文件大小
    private Double startTime;   //开始时间
    private Double endTime;     //结束时间
    private Integer dischargeCount; //异常放电次数
    private String rhythm;  //是否规则
    private String frequency;   //波形特性
    private Integer riskLevel;      //危险系数
    private List<Anomaly> anomalies; // 异常列表
    private Integer patientId;  //患者id
    private Integer userId; //医生id

    // 新增关联字段
    private String patientName;    // 患者姓名（来自 patient 表）
    private String doctorName;     // 医生姓名（来自 users 表）
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime createTime;
}