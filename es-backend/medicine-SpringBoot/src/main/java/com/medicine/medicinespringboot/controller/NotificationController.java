package com.medicine.medicinespringboot.controller;


import com.medicine.medicinespringboot.pojo.Notification;
import com.medicine.medicinespringboot.pojo.Result;
import com.medicine.medicinespringboot.pojo.User;
import com.medicine.medicinespringboot.service.Impl.NotificationService;
import com.medicine.medicinespringboot.service.Impl.UserService;
import com.medicine.medicinespringboot.utils.ThreadLocalUtil;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;


import java.util.List;
import java.util.Map;


@Slf4j
@RestController
@RequestMapping("/notification")
public class NotificationController {
    @Autowired
    private NotificationService notificationService;
    @Autowired
    private UserService userService;


    @PostMapping
    public Result add(@RequestBody Notification notification){
        Map<String,Object> map = ThreadLocalUtil.get();
        String username = (String) map.get("username");
        User user = userService.findByUsername(username);
        notification.setUserId(Long.valueOf(user.getId()));
        notificationService.add(notification);
        log.info("用户{},添加通知{}",username,notification);
        return Result.success();
    }

    @GetMapping("/list")
    public Result<List<Notification>> list(){
        Map<String,Object> map = ThreadLocalUtil.get();
        log.info("用户{},查看通知",map.get("username"));
        List<Notification> list =  notificationService.list();
        return Result.success(list);
    }




}
