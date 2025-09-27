
import React, { useState, useEffect } from 'react';
import { 
  Table, 
  Card, 
  Button, 
  Space, 
  Input, 
  Select, 
  Tag, 
  Avatar, 
  Tooltip,
  Modal,
  Form,
  message,
  Popconfirm
} from 'antd';
import { 
  PlusOutlined, 
  SearchOutlined, 
  EditOutlined, 
  DeleteOutlined,
  UserOutlined,
  MailOutlined,
  PhoneOutlined
} from '@ant-design/icons';
import apiService from '../../services/api';

const { Option } = Select;

interface Customer {
  id: string;
  name: string;
  email: string;
  phone: string;
  company: string;
  industry: string;
  status: 'active' | 'inactive' | 'prospect';
  created_at: string;
}

const CustomersList: React.FC = () => {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingCustomer, setEditingCustomer] = useState<Customer | null>(null);
  const [searchText, setSearchText] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [form] = Form.useForm();

  useEffect(() => {
    loadCustomers();
  }, []);

  const loadCustomers = async () => {
    setLoading(true);
    try {
      const response = await apiService.getCustomers();
      setCustomers(response);
    } catch (error) {
      message.error('Failed to load customers');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateCustomer = () => {
    setEditingCustomer(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEditCustomer = (customer: Customer) => {
    setEditingCustomer(customer);
    form.setFieldsValue(customer);
    setModalVisible(true);
  };

  const handleDeleteCustomer = async (customerId: string) => {
    try {
      await apiService.deleteCustomer(customerId);
      message.success('Customer deleted successfully');
      loadCustomers();
    } catch (error) {
      message.error('Failed to delete customer');
    }
  };

  const handleSubmit = async (values: any) => {
    try {
      if (editingCustomer) {
        await apiService.updateCustomer(editingCustomer.id, values);
        message.success('Customer updated successfully');
      } else {
        await apiService.createCustomer(values);
        message.success('Customer created successfully');
      }
      setModalVisible(false);
      loadCustomers();
    } catch (error) {
      message.error('Operation failed');
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'green';
      case 'inactive': return 'red';
      case 'prospect': return 'blue';
      default: return 'default';
    }
  };

  const columns = [
    {
      title: 'Customer',
      key: 'customer',
      render: (record: Customer) => (
        <Space>
          <Avatar icon={<UserOutlined />} />
          <div>
            <div style={{ fontWeight: 500 }}>{record.name}</div>
            <div style={{ fontSize: '12px', color: '#666' }}>{record.company}</div>
          </div>
        </Space>
      ),
    },
    {
      title: 'Contact',
      key: 'contact',
      render: (record: Customer) => (
        <Space direction="vertical" size="small">
          <Space size="small">
            <MailOutlined style={{ color: '#666' }} />
            <span>{record.email}</span>
          </Space>
          <Space size="small">
            <PhoneOutlined style={{ color: '#666' }} />
            <span>{record.phone}</span>
          </Space>
        </Space>
      ),
    },
    {
      title: 'Industry',
      dataIndex: 'industry',
      key: 'industry',
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => (
        <Tag color={getStatusColor(status)}>
          {status.toUpperCase()}
        </Tag>
      ),
    },
    {
      title: 'Created',
      dataIndex: 'created_at',
      key: 'created_at',
      render: (date: string) => new Date(date).toLocaleDateString(),
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (record: Customer) => (
        <Space>
          <Tooltip title="Edit">
            <Button 
              type="text" 
              icon={<EditOutlined />} 
              onClick={() => handleEditCustomer(record)}
            />
          </Tooltip>
          <Popconfirm
            title="Are you sure you want to delete this customer?"
            onConfirm={() => handleDeleteCustomer(record.id)}
            okText="Yes"
            cancelText="No"
          >
            <Tooltip title="Delete">
              <Button type="text" danger icon={<DeleteOutlined />} />
            </Tooltip>
          </Popconfirm>
        </Space>
      ),
    },
  ];

  const filteredCustomers = customers.filter(customer => {
    const matchesSearch = customer.name.toLowerCase().includes(searchText.toLowerCase()) ||
                         customer.email.toLowerCase().includes(searchText.toLowerCase()) ||
                         customer.company.toLowerCase().includes(searchText.toLowerCase());
    const matchesStatus = statusFilter === 'all' || customer.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  return (
    <Card>
      <div style={{ marginBottom: 16, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Space size="middle">
          <Input
            placeholder="Search customers..."
            prefix={<SearchOutlined />}
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
            style={{ width: 300 }}
          />
          <Select
            value={statusFilter}
            onChange={setStatusFilter}
            style={{ width: 120 }}
          >
            <Option value="all">All Status</Option>
            <Option value="active">Active</Option>
            <Option value="inactive">Inactive</Option>
            <Option value="prospect">Prospect</Option>
          </Select>
        </Space>
        <Button 
          type="primary" 
          icon={<PlusOutlined />}
          onClick={handleCreateCustomer}
        >
          Add Customer
        </Button>
      </div>

      <Table
        columns={columns}
        dataSource={filteredCustomers}
        loading={loading}
        rowKey="id"
        pagination={{
          pageSize: 10,
          showSizeChanger: true,
          showQuickJumper: true,
          showTotal: (total, range) => `${range[0]}-${range[1]} of ${total} customers`,
        }}
      />

      <Modal
        title={editingCustomer ? 'Edit Customer' : 'Add New Customer'}
        open={modalVisible}
        onCancel={() => setModalVisible(false)}
        footer={null}
        width={600}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
        >
          <Form.Item
            name="name"
            label="Customer Name"
            rules={[{ required: true, message: 'Please enter customer name' }]}
          >
            <Input />
          </Form.Item>
          
          <Form.Item
            name="email"
            label="Email"
            rules={[
              { required: true, message: 'Please enter email' },
              { type: 'email', message: 'Please enter a valid email' }
            ]}
          >
            <Input />
          </Form.Item>
          
          <Form.Item
            name="phone"
            label="Phone"
          >
            <Input />
          </Form.Item>
          
          <Form.Item
            name="company"
            label="Company"
            rules={[{ required: true, message: 'Please enter company name' }]}
          >
            <Input />
          </Form.Item>
          
          <Form.Item
            name="industry"
            label="Industry"
          >
            <Input />
          </Form.Item>
          
          <Form.Item
            name="status"
            label="Status"
            initialValue="prospect"
          >
            <Select>
              <Option value="active">Active</Option>
              <Option value="inactive">Inactive</Option>
              <Option value="prospect">Prospect</Option>
            </Select>
          </Form.Item>

          <Form.Item style={{ marginBottom: 0, textAlign: 'right' }}>
            <Space>
              <Button onClick={() => setModalVisible(false)}>
                Cancel
              </Button>
              <Button type="primary" htmlType="submit">
                {editingCustomer ? 'Update' : 'Create'}
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>
    </Card>
  );
};

export default CustomersList;
