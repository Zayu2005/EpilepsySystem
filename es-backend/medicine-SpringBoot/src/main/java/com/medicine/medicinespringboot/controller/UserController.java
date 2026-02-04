package com.medicine.medicinespringboot.controller;


import com.medicine.medicinespringboot.pojo.PageBean;
import com.medicine.medicinespringboot.pojo.Result;
import com.medicine.medicinespringboot.pojo.User;
import com.medicine.medicinespringboot.service.Impl.UserService;

import com.medicine.medicinespringboot.utils.JwtUtil;
import com.medicine.medicinespringboot.utils.Md5Util;
import com.medicine.medicinespringboot.utils.ThreadLocalUtil;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;
import java.util.Objects;

@Slf4j
@RestController
@RequestMapping("/user")
public class UserController {

    @Autowired
    private UserService userService;


    @PostMapping("/register")
    public Result register(@RequestBody User user){
        String username = user.getUsername();
        if (userService.findByUsername(username) != null) {
            return Result.error("用户名已存在");
        }
        String password = user.getPassword();
        System.out.println(password);
        String md5Password = Md5Util.getMD5String(password);
        user.setPassword(md5Password);
        user.setUserStatus(1);
        userService.add(user);
        return Result.success();
    }


    @PostMapping("/update")
    public Result update(@RequestBody User user) {
        Map<String, Object> map = ThreadLocalUtil.get();
        String username = (String) map.get("username");
        if (!Objects.equals(username, "admin")) {
            return Result.error("权限不足");
        }
        userService.updateInfo(user);
        return Result.success();
    }
    @PostMapping("/login")
    public Result login(String username, String password) {

        User loginUser = userService.findByUsername(username);

        if (loginUser == null) {
            return Result.error("用户名或密码错误");
        }
        if(loginUser.getUserStatus() == 0)
            return Result.error("用户被禁用,请联系管理员");
        if (Md5Util.getMD5String(password).equals(loginUser.getPassword())) {
            log.info("用户:{},登录成功", loginUser.getUsername());
            Map<String, Object> claims = new HashMap<>();
            claims.put("id", loginUser.getId());
            claims.put("username", loginUser.getUsername());
            String token = JwtUtil.genToken(claims);
            return Result.success(token);
        }
        return Result.error("用户名或密码错误");
    }




    @GetMapping("/info")
    public Result<User> info() {
        Map<String, Object> map = ThreadLocalUtil.get();
        String username = (String) map.get("username");
        User user = userService.findByUsername(username);
        return Result.success(user);
    }

    @GetMapping("/count")
    public Result<Integer> count() {
        Integer count = userService.count();
        Map<String, Object> map = ThreadLocalUtil.get();
        String username = (String) map.get("username");
        log.info("用户{},查询在院患者为:{}",username,count);
        return Result.success(count);
    }

    @GetMapping("/list")
    public Result<PageBean<User>> list(
            Integer pageNum,
            Integer pageSize,
            @RequestParam(required = false) String name,
            @RequestParam(required = false) Integer status
    ){
        Map<String, Object> map = ThreadLocalUtil.get();
        String username = (String) map.get("username");
//        if(!Objects.equals(username, "admin")){
//            return Result.error("权限不足");
//        }
        log.info("用户{},进行多页查询,pageNum:{},pageSize{}", username, pageNum, pageSize);
        PageBean<User> pageBean = userService.list(pageNum, pageSize, name, status);
        return Result.success(pageBean);
    }

    @PostMapping("/status")
    public Result status(@RequestBody User user){
        Map<String, Object> map = ThreadLocalUtil.get();
        String username = (String) map.get("username");
        if(!Objects.equals(username, "admin")){
            return Result.error("权限不足");
        }
        log.info("用户{},进行状态修改,user:{}", username, user);
        User user1 = userService.findById(user.getId());
        if(user1.getId().equals("1")){
            return Result.error("管理员状态不可修改");
        }
        userService.update(user);
        return Result.success();
    }
}
