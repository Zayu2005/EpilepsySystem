//package com.medicine.medicinespringboot.utils;
//
//import com.medicine.medicinespringboot.service.Impl.PatientService;
//import org.springframework.ai.tool.annotation.Tool;
//import org.springframework.beans.factory.annotation.Autowired;
//import org.springframework.context.annotation.ComponentScan;
//import org.springframework.context.i18n.LocaleContextHolder;
//import org.springframework.stereotype.Component;
//import org.springframework.stereotype.Service;
//
//import java.time.LocalDateTime;
//
//
//@Component
//public class AiChatTools {
//    @Autowired
//    private PatientService patientService;
//
//    @Tool(description = "获得当前的日期时间")
//    String getCurrentDateTime() {
//        return LocalDateTime.now().atZone(LocaleContextHolder.getTimeZone().toZoneId()).toString();
//    }
//
//    @Tool(description = "获得当前所有患者或病人的数量")
//    Integer getCurrentPatientCount(){
//        return patientService.count();
//    }
//}
//
