package com.medicine.medicinespringboot.service.Impl;

import com.medicine.medicinespringboot.pojo.PageBean;
import com.medicine.medicinespringboot.pojo.Todo;

public interface TodoService {
    void add(Todo todo);

    PageBean<Todo> list(Integer pageNum, Integer pageSize, Integer completed, Integer userId);

    Todo findTodoById(Integer id);

    void delete(Integer id);

    void update(Todo todo);
}
