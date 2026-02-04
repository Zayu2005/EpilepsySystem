package com.medicine.medicinespringboot.mapper;


import com.medicine.medicinespringboot.pojo.Notification;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface NotificationMapper {


    @Insert("insert into notification(user_id, title, content, create_time, update_time)" +
            "VALUES (#{userId}, #{title}, #{content},NOW(), NOW())")
    void add(Notification notification);


    @Select("SELECT * FROM notification ORDER BY create_time DESC ")
    List<Notification> list();
}
