package com.medicine.medicinespringboot.pojo;

import lombok.Data;

@Data
public class Anomaly {
    private Integer id; //id
    private Integer analysisId; // 外键关联主表ID
    private String type;    //波形类型
    private String severity;
}