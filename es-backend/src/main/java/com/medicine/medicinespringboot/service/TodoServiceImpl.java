package com.medicine.medicinespringboot.service;

import com.github.pagehelper.Page;
import com.github.pagehelper.PageHelper;
import com.medicine.medicinespringboot.mapper.TodoMapper;
import com.medicine.medicinespringboot.pojo.PageBean;
import com.medicine.medicinespringboot.pojo.Todo;
import com.medicine.medicinespringboot.service.Impl.TodoService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;


@Service
public class TodoServiceImpl implements TodoService {

    @Autowired
    private TodoMapper todoMapper;

    @Override
    public void add(Todo todo) {
        todoMapper.add(todo);
    }

    @Override
    public PageBean<Todo> list(Integer pageNum, Integer pageSize, Integer completed, Integer userId) {
        //创建PageBean对象
        PageBean<Todo> pageBean = new PageBean<>();
        //开启非也查询 pageHelper
        PageHelper.startPage(pageNum, pageSize);
        //调用mapper层
        List<Todo> todoList = todoMapper.list(completed, userId);
        //获取总记录数和总页数
        Page<Todo> page = (Page<Todo>) todoList;
        //数据填充
        pageBean.setTotal(page.getTotal());
        pageBean.setItems(page.getResult());
        return pageBean;
    }

    @Override
    public Todo findTodoById(Integer id) {
        return todoMapper.findTodoById(id);
    }

    @Override
    public void delete(Integer id) {
        todoMapper.delete(id);
    }

    @Override
    public void update(Todo todo) {
        todoMapper.update(todo);
    }
}
