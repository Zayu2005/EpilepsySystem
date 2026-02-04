package com.medicine.medicinespringboot.service;

import com.github.pagehelper.Page;
import com.github.pagehelper.PageHelper;
import com.medicine.medicinespringboot.mapper.UserMapper;
import com.medicine.medicinespringboot.pojo.PageBean;
import com.medicine.medicinespringboot.pojo.User;
import com.medicine.medicinespringboot.service.Impl.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class UserServiceImpl implements UserService {



    @Autowired
    private UserMapper userMapper;

    @Override
    public User findByUsername(String username) {
        return userMapper.findByUsername(username);
    }

    @Override
    public Integer count() {
        return userMapper.count();
    }

    @Override
    public PageBean<User> list(Integer pageNum, Integer pageSize, String name, Integer status) {
        //创建PageBean对象
        PageBean<User> pageBean = new PageBean<>();
        //开启分页查询 pageHelper
        PageHelper.startPage(pageNum, pageSize);
        //调用mapper层
        List<User> userList = userMapper.list(name, status);
        //获取总记录数和总页数
        Page<User> page = (Page<User>) userList;
        //数据填充
        pageBean.setTotal(page.getTotal());
        pageBean.setItems(page.getResult());
        return pageBean;
    }

    @Override
    public User findById(String id) {
        return userMapper.findById(id);
    }

    @Override
    public void update(User user) {
        userMapper.update(user);
    }

    @Override
    public void add(User user) {
        userMapper.add(user);
    }

    @Override
    public void updateInfo(User user) {
        userMapper.updateInfo(user);
    }
}
