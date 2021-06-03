#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

static double find_distance(double *dot, double *center, int d){
    double dis;
    int i;
    dis = 0;

    for ( i = 0; i < d; i++)
        dis += (dot[i] - center[i]) * (dot[i] - center[i]);
    return  dis;

}
static int get_index_of_closest_cluster(double* dot, double** cluster_list, int d, int k )
{
    int j;
    int i;
    double min_dis;
    double tmp_dis;
    j = 0;
    min_dis = find_distance(dot, cluster_list[0], d);

    for (i = 1; i < k; i++)
    {
        tmp_dis = find_distance(dot, cluster_list[i], d);
        if (tmp_dis <= min_dis)
        {
            min_dis = tmp_dis;
            j = i;
        }
    }
    return j;
}
static void update_cluster_center(double* dot, double * center,int cluster_size,int d,int sign) {
    double* center_temp;
    int i;
    if (cluster_size+sign==0)
        printf("error \n ");

    center_temp  = (double *) calloc(d,sizeof(double ));
    for (i = 0; i < d; i++)
        center_temp[i] = (center[i] * (cluster_size));

    for (i = 0; i < d; i++){
        center_temp[i] += (dot[i]*sign);
        center[i] = center_temp[i] / (cluster_size+sign);

    }
}


static  void simple_kmean (double ** dot_list, double ** cluster_list,double * cluster_index_list, int n,int k,int d,int max_iter) {
    int i,j;
    int *dot_at;
    int *move_dot_to;
    int *cluster_size;

    int is_a_cluster_changed;
    int count_iter;

    dot_at = (int*) calloc(n,sizeof (int));
    move_dot_to = (int*) calloc(n,sizeof (int));
    cluster_size = (int*) calloc(k,sizeof (int));


    for (i = 0; i < n; i++) {
        dot_at[i] = -1;
        move_dot_to[i] = 0;
    }
    for (i = 0; i < k; i++) {
        j = (int) cluster_index_list[i];
        dot_at[j] = i;
        cluster_size[j] = 1;

    }


    is_a_cluster_changed = 1;
    count_iter = 0;
    while (count_iter < max_iter && is_a_cluster_changed) {
        int i, j;
        is_a_cluster_changed = 0;
        count_iter++;

        for (i = 0; i < n; i++) /*find nearest clusters */
            move_dot_to[i] = get_index_of_closest_cluster(dot_list[i], cluster_list, d, k);

        for (j = 0; j < n; j++) {/* update clusters*/
            if (dot_at[j] == -1) {
                dot_at[j] = move_dot_to[j];
                update_cluster_center(dot_list[j], cluster_list[move_dot_to[j]], cluster_size[move_dot_to[j]], d,1); /*add dot to center*/
                cluster_size[move_dot_to[j]]++;
                is_a_cluster_changed = 1;
            } else {
                if (dot_at[j] != move_dot_to[j]) {
                    update_cluster_center(dot_list[j], cluster_list[dot_at[j]], cluster_size[dot_at[j]], d,
                                          -1); /*remove dot from center */
                    update_cluster_center(dot_list[j], cluster_list[move_dot_to[j]], cluster_size[move_dot_to[j]], d,
                                          1); /*add dot to center */
                    cluster_size[dot_at[j]]--;
                    cluster_size[move_dot_to[j]]++;
                    dot_at[j] = move_dot_to[j];
                    is_a_cluster_changed = 1;
                }
            }
        }
    }

    /* print_matrix(cluster_list, k, d); */
    free(dot_at);
    free(move_dot_to);
    free(cluster_size);

}


/* ************  API FUNCTION CONVERT PYTHON OBJECT INTO C ARRAY AND BACK ************ */
static void check_for_py_list(PyObject * _list)
{
   assert (!PyList_Check(_list) && "this is not a list ");
}

static void print_dots_list(double ** list, Py_ssize_t n, Py_ssize_t d )
{
    Py_ssize_t i;
    /*printf("[") ; */
     for (i = 0; i < n; i++)
     {
     /*    printf("[") ;
        for (j = 0; j < d; j++)         {
          printf("%.4lf , ", list[i][j]) ;
          }
     printf("]\n") ;*/
     free(list[i]);

    }
   /* printf("]") ; */
    free(list);
}

static  PyObject* get_py_lst_from_c_array(double* c_dot, Py_ssize_t  d)
{
    Py_ssize_t i;
    PyObject * dot ;
    PyObject* item;
    dot = PyList_New(d); /* https://docs.python.org/3/c-api/list.html */
        for (i = 0; i < d; i++) {
        item = PyFloat_FromDouble(c_dot[i]) ;
        PyList_SetItem(dot,i,item);
        // TO DO FREE MEMORY
    }
    return dot;
 }

static PyObject* get_py_lst_from_c_matrix(double ** c_dot_list ,  Py_ssize_t n, Py_ssize_t d)
{
   Py_ssize_t i;
   PyObject * dot_list ;
   PyObject* dot;

   dot_list = PyList_New(n);
  for (i = 0; i < n; i++)
     {
      dot = get_py_lst_from_c_array(c_dot_list[i],d);
      PyList_SetItem(dot_list,i,dot);
     }
    // TO DO FREE MEMORY
    return dot_list;

}


static  double* get_c_array_from_py_lst(PyObject * list, Py_ssize_t  d)
{
    Py_ssize_t i;
    PyObject *item;
    /* NEVER EVER USE malloc/calloc/realloc or free on PyObject */
      double *c_dot = malloc(sizeof(double) * d);
      assert(c_dot != NULL && "Problem in  load_python_list_to_c_array");
        for (i = 0; i < d; i++) {
        item = PyList_GetItem(list, i);
        c_dot[i] =  PyFloat_AsDouble((item));

        if (c_dot[i]  == -1 && PyErr_Occurred()){
            puts("Something bad ...");
            free(c_dot);
            return c_dot;
         }

    }
    return c_dot;
}


static double** get_c_matrix_from_py_lst(PyObject * _list,  Py_ssize_t n, Py_ssize_t d)
{

   Py_ssize_t i;
   PyObject  *item;
   double ** c_dot_list;
   c_dot_list = (double **) malloc( n* sizeof(double *));
   check_for_py_list(_list);
   assert(c_dot_list != NULL && "Problem in  load_python_list_to_c_array");


     for (i = 0; i < n; i++)
     {
        item = PyList_GetItem(_list, i);
         if (!PyList_Check(item)){ continue;}
         c_dot_list[i] = get_c_array_from_py_lst(item,d);
    }
    return c_dot_list;

}

/* ************  API FUNCTION CONVERT PYTHON OBJECT INTO C ARRAY AND BACK ************ */


/*
 * API functions
 */


/*
 * Print list of lists of ints without changing it
 */
static PyObject* fit(PyObject *self, PyObject *args)
{
    PyObject *_dots_list,*_cluster_list,*_cluster_index_list;
    Py_ssize_t n,k, d;
    int max_iter;
    double ** c_dot_list;
    double ** c_cluster_list;
    double * c_cluster_index_list;

    if(!PyArg_ParseTuple(args, "iOOO",&max_iter, &_dots_list,&_cluster_list,&_cluster_index_list)) { return NULL;}

    check_for_py_list(_dots_list);
    check_for_py_list(_cluster_list);
    check_for_py_list(_cluster_index_list);

     n = PyList_Size(_dots_list);
     k = PyList_Size(_cluster_list);
     d = PyList_Size(PyList_GetItem(_dots_list, 0));


    c_dot_list = get_c_matrix_from_py_lst(_dots_list,n,d);
    c_cluster_list = get_c_matrix_from_py_lst(_cluster_list,k,d);
    c_cluster_index_list = get_c_array_from_py_lst(_cluster_index_list,k);


    simple_kmean(c_dot_list, c_cluster_list ,c_cluster_index_list,(int) n, (int)k,(int) d,max_iter );

    _cluster_list =  get_py_lst_from_c_matrix(c_cluster_list ,k,d, max_iter);


    print_dots_list(c_dot_list,n,d); //this free the memory !

    print_dots_list(c_cluster_list,k,d); //this free the memory !

    return _cluster_list;

}

/*
 * A macro to help us with defining the methods
 * Compare with: {"f1", (PyCFunction)f1, METH_NOARGS, PyDoc_STR("No input parameters")}
*/
#define FUNC(_flag, _name, _docstring) { #_name, (PyCFunction)_name, _flag, PyDoc_STR(_docstring) }

static PyMethodDef _methods[] = {
    FUNC(METH_VARARGS, fit, "Print list of lists of ints without changing it"),
    {NULL, NULL, 0, NULL}   /* sentinel */
};

static struct PyModuleDef _moduledef = {
    PyModuleDef_HEAD_INIT,
    "mykmeanssp",
    NULL,
    -1,
    _methods
};

PyMODINIT_FUNC
PyInit_mykmeanssp(void)
{
    return PyModule_Create(&_moduledef);
}


