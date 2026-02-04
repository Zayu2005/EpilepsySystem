package com.medicine.medicinespringboot.service.Impl;


import com.medicine.medicinespringboot.pojo.PageBean;
import com.medicine.medicinespringboot.pojo.Patient;

import java.util.List;

public interface PatientService {

    Integer count();

    //分页查询
    PageBean<Patient> list(Integer pageNum, Integer pageSize, String name);

    void delete(Integer id);

    void add(Patient patient);

    void update(Patient patient);

    List<Patient> all();


    void diagnosis(Patient patient);

    Patient findPatientByName(String name);
}
