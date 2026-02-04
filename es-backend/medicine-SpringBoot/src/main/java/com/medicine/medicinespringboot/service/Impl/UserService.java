package com.medicine.medicinespringboot.service.Impl;

import com.medicine.medicinespringboot.pojo.PageBean;
import com.medicine.medicinespringboot.pojo.User;
import org.springframework.stereotype.Service;


public interface UserService {
    User findByUsername(String username);

    Integer count();

    PageBean<User> list(Integer pageNum, Integer pageSize, String name, Integer status);

    User findById(String id);

    void update(User user);

    void add(User user);

    void updateInfo(User user);
}
