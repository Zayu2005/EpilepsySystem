package com.medicine.medicinespringboot.pojo;


import lombok.Data;

@Data
public class EegFeaturesFile {

    private Integer id; //文件id编号
    private Integer patientId;  //病人id
    private Integer userId; //医生id
    private String url; //文件地址
}
