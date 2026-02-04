package com.medicine.medicinespringboot.pojo;

import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.Data;
import org.springframework.format.annotation.DateTimeFormat;

import java.time.LocalDateTime;



@Data
public class Notification {
    private Long id;    //id
    private Long userId;    //创建人id
    private String title;   //标题
    private String content; //内容
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime createTime;   //创建时间
    private LocalDateTime updateTime;   //更新时间
}
