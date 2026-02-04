package com.medicine.medicinespringboot.service;

import com.github.pagehelper.Page;
import com.github.pagehelper.PageHelper;
import com.medicine.medicinespringboot.mapper.PatientMapper;
import com.medicine.medicinespringboot.pojo.PageBean;
import com.medicine.medicinespringboot.pojo.Patient;
import com.medicine.medicinespringboot.service.Impl.PatientService;
import com.medicine.medicinespringboot.utils.ThreadLocalUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;


@Service
public class PatientServiceImpl implements PatientService {
    @Autowired
    private PatientMapper patientMapper;

    public Integer count() {
        return patientMapper.count();
    }

    @Override
    public PageBean<Patient> list(Integer pageNum, Integer pageSize, String name) {
        //创建PageBean对象
        PageBean<Patient> pageBean = new PageBean<>();
        //开启分页查询 pageHelper
        PageHelper.startPage(pageNum, pageSize);
        //调用mapper层
        List<Patient> patientsList = patientMapper.list(name);
        //page中提供了方法，获取总记录数和总页数
        Page<Patient> page = (Page<Patient>) patientsList;
        //把数据填充到PageBean对象中
        pageBean.setTotal(page.getTotal());
        pageBean.setItems(page.getResult());
        return pageBean;
    }

    //删除
    @Override
    public void delete(Integer id) {
        patientMapper.delete(id);
    }

    @Override
    public void add(Patient patient) {
        patientMapper.add(patient);
    }

    @Override
    public void update(Patient patient) {
        patientMapper.update(patient);
    }

    @Override
    public List<Patient> all() {
        return patientMapper.all();
    }

    @Override
    public void diagnosis(Patient patient) {
        patientMapper.diagnosis(patient);
    }

    @Override
    public Patient findPatientByName(String name) {
        return patientMapper.findPatientByName(name);
    }


}
