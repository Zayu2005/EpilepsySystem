package com.medicine.medicinespringboot.mapper;


import com.medicine.medicinespringboot.pojo.User;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;

import java.util.List;

@Mapper
public interface UserMapper {


    @Select("select * from users where username = #{username}")
    public User findByUsername(String username);

    @Select("select count(*) from patient")
    Integer count();

    List<User> list(String name, Integer status);

    @Select("select * from users where id = #{id}")
    User findById(String id);


    @Update("update users set user_status = #{userStatus} where id = #{id}")
    void update(User user);


    @Insert("insert into users (username,name,password,user_status,phone,email,create_time,update_time)" +
            "VALUES (#{username}, #{name}, #{password}, #{userStatus}, #{phone}, #{email}, now(),now())")
    void add(User user);


    @Update("update users set username = #{username},name = #{name},phone = #{phone},email = #{email},update_time = now() where id = #{id}")
    void updateInfo(User user);
}
