#include<iostream>
#include<string.h>
using namespace std;


//并不是为了对p的深度copy，在复制类对象
// 是为了演示，对数据地址p的引用过程
//1.无论a被复制多少份，数据指针永远都是同一个。/
//使得这个数据不至于有太多副本
class A{
pubilc:

	A(){
		this->p =new int[100];
		this->p[0] = 555;
		
	}
	//深拷贝的实现(拷贝构造函数)
	A(const A& other){
		this ->a= other.a;
		this ->b =other.b;
		this ->p = new int[100];
		memcpy(this->p,other.p,sizeof(int)*100)
		
	}

	virtual ~A(){
	//当最后一个引用实例释放时，删除p指针
	//怎么判断目前执行的析构函数是最沟一个呢？
		delete [] this->p;
	}

	int a=123;
	int b=234;
	int* p =nullptr;
}







int main(){

	A a;
	A b=a;
	cout<<a.p<<endl;
	cout<<b.p<<endl;
	return 0;
}







#include<iostream>
#include<cmath>
#include<memory>

using namespace std;



//表达式类
//1.所有的操作都可以认为是表达式
//	a.标量x，可以认为是标量表达式
//  b.任意的算子，比如加减乘除，都可以抽象为表达式


//储存表达式所需要的相关数据
//因为只存储数据不执行操作，所以要定义成纯虚类
class Container(){
public:
	
	//返回这个表达式具体类型或名称
	virtual const char* type() = 0;
	
	//forward实现过程
	virtual float forward() = 0;
	
	//具体的backward实现
	virtual void backward(float gradient) = 0;
}





class Expression{
public:

	//对该表达式进行前向推理，并得到推理结果
	float forward(){
		return container_->forward();
	}
	//对该表达式进行反响推理，并计算每一个节点的导数
	void backward(){
		return container_->backward(1.0f);
	
	}
	
	//为了储存表达式中的数据，索引需要引入二级指针,表达式所储存的具体实现
	//具体实现在这里
	shared_ptr<Container> container_;
};



class ScalarContainer : public Container{
public:
	ScalarContainer(float value){
		value_ = value;
	}
	//返回这个表达式具体类型或名称
	virtual const char* type() override{
		return "Scalar";
	
	//forward实现过程
	virtual float forward() override{
		return value_;
	}
	//具体的backward实现
	virtual void backward(float gradient) override{
		gradient_+=gradient
	}
	float value_ = 0;
	float gradient_ = 0;
};


class MultiplyContainer : public Container{
public:
	MultiplyContainer(const Expression& left,const Expression& right){
		left_value_ = left.container_;
		right_value_ = left.container_;
	}
	//返回这个表达式具体类型或名称
	virtual const char* type() override{
		return "Multipy";
	
	//forward实现过程
	virtual float forward() override{
		return left_value->forward()* right_value->forward;
	}
	//具体的backward实现
	virtual void backward(float gradient) override{
		left_value_->backward(gradient *right_value_ ->forwaed())
		right_value_->backward(gradient *right_value_ ->forwaed())
	}
	shared_ptr<Container> left_value_;
	shared_ptr<Container> right_value_;
};

class Scalar: public Expression{
public:
	Scalar(float value){
		container_.reset(new ScalarContainer(value));
	}
};



class Multiply: public Expression{
public:
	Multiply(const Expression& left,const Expression& right ){
		return container_.reset(new ScalarContainer(left , right));
	}
};






int main(){
	
	
	//a是一个通过调整得到的值
	//x是一个常量，需要求解的对象
	
	float x=9;
	Scalar a(x/2.0f);
	//auto loss = (a.power()-x).power()
	cout<< a.forward() <<endl;
	
	return 0;

}


























