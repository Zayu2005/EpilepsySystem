package com.medicine.medicinespringboot.mapper;


import com.medicine.medicinespringboot.pojo.Patient;
import org.apache.ibatis.annotations.Delete;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;

import java.util.List;

@Mapper
public interface PatientMapper {


    @Select("select count(*) from patient")
    Integer count();



    List<Patient> list(String name);


    @Delete("delete from patient where id=#{id} ")
    void delete(Integer id);


    void add(Patient patient);

    @Update("update patient set name=#{name},age=#{age},male=#{male},phone=#{phone},address=#{address},doctor_id=#{doctorId},department_id=#{departmentId},text=#{text},update_time=#{updateTime} where id=#{id}")
    void update(Patient patient);



    @Select("select * from patient")
    List<Patient> all();


    @Update("update patient set diagnosis=#{diagnosis},text = #{text},update_time = NOW() where id=#{id}")
    void diagnosis(Patient patient);

    @Select("select * from patient where name=#{name}")
    Patient findPatientByName(String name);
}
