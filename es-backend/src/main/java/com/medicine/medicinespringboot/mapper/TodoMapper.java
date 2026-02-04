package com.medicine.medicinespringboot.mapper;


import com.medicine.medicinespringboot.pojo.Todo;
import org.apache.ibatis.annotations.*;

import java.util.List;

@Mapper
public interface TodoMapper {




    @Insert("insert into todo (content,time,type,completed,user_id,create_time,update_time) values (#{content},#{time},#{type},#{completed},#{userId},now(),now())")
    void add(Todo todo);


    List<Todo> list(Integer completed, Integer userId);



    @Select("select * from todo where id = #{id}")
    Todo findTodoById(Integer id);


    @Delete("delete from todo where id = #{id}")
    void delete(Integer id);

    @Update("update todo set completed = #{completed},update_time = now() where id = #{id}")
    void update(Todo todo);
}
