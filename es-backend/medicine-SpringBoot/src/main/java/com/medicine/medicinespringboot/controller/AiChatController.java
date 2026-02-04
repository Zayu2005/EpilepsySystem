//package com.medicine.medicinespringboot.controller;
//
//
//import com.medicine.medicinespringboot.pojo.Patient;
//import com.medicine.medicinespringboot.service.Impl.PatientService;
//import org.springframework.ai.tool.annotation.Tool;
//import org.springframework.ai.tool.annotation.ToolParam;
//import org.springframework.beans.factory.annotation.Autowired;
//import org.springframework.context.i18n.LocaleContextHolder;
//import org.springframework.stereotype.Controller;
//
//import java.time.LocalDateTime;
//import java.util.List;
//
//@Controller
//public class AiChatController {
//
//    @Autowired
//    private PatientService patientService;
//
//    @Tool(description = "获取当前的日期时间")
//    String getCurrentDateTime() {
//        return LocalDateTime.now().atZone(LocaleContextHolder.getTimeZone().toZoneId()).toString();
//    }
//
//    @Tool(description = "获取当前患者的数量")
//    Integer getPatientCount() {
//        return patientService.count();
//    }
//
//    @Tool(description = "获取所有患者")
//    List<Patient> getAllPatients() {
//        return patientService.all();
//    }
//
//
//    @Tool(description = "查询病人信息")
//    Patient getPatient(@ToolParam(description = "病人名") String name) {
//        return patientService.findPatientByName(name);
//    }
//
//
//
//}
