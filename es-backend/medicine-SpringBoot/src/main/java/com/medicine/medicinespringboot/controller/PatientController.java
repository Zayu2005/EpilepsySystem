package com.medicine.medicinespringboot.controller;
import com.medicine.medicinespringboot.pojo.PageBean;
import com.medicine.medicinespringboot.pojo.Patient;
import com.medicine.medicinespringboot.pojo.Result;
import com.medicine.medicinespringboot.service.Impl.PatientService;
import com.medicine.medicinespringboot.utils.ThreadLocalUtil;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;


@Slf4j
@RestController
@RequestMapping("/patient")
public class PatientController {

    @Autowired
    private PatientService patientService;

    @GetMapping("/count")
    public Result<Integer> count() {
        return Result.success(patientService.count());
    }
    @GetMapping("/all")
    public Result<List<Patient>> all(){
        Map<String, Object> claims = ThreadLocalUtil.get();
        log.info("用户{},查询所有患者",claims.get("username"));
        List<Patient> list =  patientService.all();
        return Result.success(list);
    }

    //分页查询
    @GetMapping
    public Result<PageBean<Patient>> list(
            Integer pageNum,
            Integer pageSize,
            @RequestParam(required = false) String name
    ) {
        Map<String, Object> claims = ThreadLocalUtil.get();
        String username = (String) claims.get("username");
        log.info("用户{},进行多页查询,pageNum:{},pageSize{}", username, pageNum, pageSize);
        PageBean<Patient> pageBean = patientService.list(pageNum, pageSize, name);
        return Result.success(pageBean);
    }

    //删除指定id
    @DeleteMapping
    public Result delete(@RequestParam(required = true) Integer id) {
        Map<String, Object> claims = ThreadLocalUtil.get();
        String username = (String) claims.get("username");
        log.info("用户{}进行操作,删除患者id为:{}", username, id);
        patientService.delete(id);
        return Result.success();
    }

    //使用路径参数添加病人
    @PostMapping
    public Result add(@RequestBody @Validated Patient  patient){
        Map<String, Object> claims = ThreadLocalUtil.get();
        String username = (String) claims.get("username");
        log.info("用户{}进行操作,添加患者信息:{}", username, patient);
        patientService.add(patient);
        return Result.success();
    }

    @PutMapping
    public Result update(@RequestBody Patient patient){
        Map<String, Object> claims = ThreadLocalUtil.get();
        String username = (String) claims.get("username");
        log.info("用户{}进行操作,修改患者信息:{}", username, patient);
        patientService.update(patient);
        return Result.success();
    }
    //填写患者病情诊断
    @PutMapping("/diagnosis")
    public Result diagnosis(@RequestBody Patient patient){
        patientService.diagnosis(patient);
        return Result.success();
    }
}
