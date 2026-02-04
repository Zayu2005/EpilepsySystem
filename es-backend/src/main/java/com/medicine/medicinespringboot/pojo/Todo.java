package com.medicine.medicinespringboot.pojo;

import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.Data;

import java.time.LocalDateTime;

@Data

public class Todo {
    private Integer id;
    private String content;
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm", timezone = "GMT+8")
    private LocalDateTime time;
    private String type;
    private Boolean completed;
    private Integer userId;
    private LocalDateTime createTime;
    private LocalDateTime updateTime;

}
