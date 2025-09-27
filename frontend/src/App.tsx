
import React, { useState, useEffect } from 'react';
import type { MenuProps } from 'antd';
import { ConfigProvider, Layout, Menu, Avatar, Dropdown, Space, Badge, Typography, Card, Row, Col, Statistic, Table, Tag } from 'antd';
import { 
  UserOutlined, 
  TeamOutlined, 
  DashboardOutlined, 
  CustomerServiceOutlined,
  UsergroupAddOutlined,
  CalendarOutlined,
  ClockCircleOutlined,
  SettingOutlined,
  LogoutOutlined,
  BellOutlined,
  SearchOutlined
} from '@ant-design/icons';
import './App.css';

const { Header, Content, Sider } = Layout;
const { Title, Text } = Typography;

type MenuItem = Required<MenuProps>['items'][number];

const menuItems: MenuItem[] = [
  {
    key: 'dashboard',
    icon: <DashboardOutlined />,
    label: 'Dashboard',
  },
  {
    key: 'crm',
    icon: <CustomerServiceOutlined />,
    label: 'CRM',
    children: [
      { key: 'customers', icon: <TeamOutlined />, label: 'Customers' },
      { key: 'leads', icon: <UsergroupAddOutlined />, label: 'Leads' },
      { key: 'opportunities', icon: <SearchOutlined />, label: 'Opportunities' },
    ],
  },
  {
    key: 'hrms',
    icon: <UserOutlined />,
    label: 'HRMS',
    children: [
      { key: 'employees', icon: <TeamOutlined />, label: 'Employees' },
      { key: 'departments', icon: <UsergroupAddOutlined />, label: 'Departments' },
      { key: 'attendance', icon: <ClockCircleOutlined />, label: 'Attendance' },
      { key: 'leave-requests', icon: <CalendarOutlined />, label: 'Leave Requests' },
    ],
  },
] as MenuItem[];

function App() {
  const [selectedKey, setSelectedKey] = useState('dashboard');
  const [collapsed, setCollapsed] = useState(false);
  const [backendStatus, setBackendStatus] = useState('checking');

  useEffect(() => {
    // Check backend connectivity
    const checkBackend = async () => {
      try {
        const response = await fetch('/api/v1/status');
        if (response.ok) {
          setBackendStatus('connected');
        } else {
          setBackendStatus('error');
        }
      } catch (error) {
        setBackendStatus('disconnected');
      }
    };
    checkBackend();
  }, []);

  const userMenu = (
    <Menu>
      <Menu.Item key="profile" icon={<UserOutlined />}>
        Profile
      </Menu.Item>
      <Menu.Item key="settings" icon={<SettingOutlined />}>
        Settings
      </Menu.Item>
      <Menu.Divider />
      <Menu.Item key="logout" icon={<LogoutOutlined />}>
        Logout
      </Menu.Item>
    </Menu>
  );

  const dashboardStats = [
    { title: 'Total Customers', value: 1254, prefix: <TeamOutlined />, color: '#1890ff' },
    { title: 'Active Leads', value: 89, prefix: <UsergroupAddOutlined />, color: '#52c41a' },
    { title: 'Total Employees', value: 156, prefix: <UserOutlined />, color: '#faad14' },
    { title: 'Pending Leaves', value: 12, prefix: <CalendarOutlined />, color: '#f5222d' },
  ];

  const recentActivities = [
    { key: '1', activity: 'New customer registered', user: 'John Doe', time: '2 hours ago', type: 'customer' },
    { key: '2', activity: 'Leave request submitted', user: 'Sarah Wilson', time: '4 hours ago', type: 'leave' },
    { key: '3', activity: 'Lead converted to customer', user: 'Mike Johnson', time: '6 hours ago', type: 'lead' },
    { key: '4', activity: 'Employee profile updated', user: 'Emma Brown', time: '1 day ago', type: 'employee' },
  ];

  const activityColumns = [
    {
      title: 'Activity',
      dataIndex: 'activity',
      key: 'activity',
    },
    {
      title: 'User',
      dataIndex: 'user',
      key: 'user',
    },
    {
      title: 'Type',
      dataIndex: 'type',
      key: 'type',
      render: (type: string) => {
        const colors = {
          customer: 'blue',
          lead: 'green',
          leave: 'orange',
          employee: 'purple'
        };
        return <Tag color={colors[type as keyof typeof colors]}>{type.toUpperCase()}</Tag>;
      },
    },
    {
      title: 'Time',
      dataIndex: 'time',
      key: 'time',
    },
  ];

  const renderDashboard = () => (
    <div>
      <Row gutter={[24, 24]} style={{ marginBottom: '24px' }}>
        {dashboardStats.map((stat, index) => (
          <Col xs={24} sm={12} lg={6} key={index}>
            <Card>
              <Statistic
                title={stat.title}
                value={stat.value}
                prefix={<span style={{ color: stat.color }}>{stat.prefix}</span>}
                valueStyle={{ color: stat.color }}
              />
            </Card>
          </Col>
        ))}
      </Row>

      <Row gutter={[24, 24]}>
        <Col xs={24} lg={16}>
          <Card title="Recent Activities" extra={<a href="/activities">View All</a>}>
            <Table 
              dataSource={recentActivities} 
              columns={activityColumns}
              pagination={false}
              size="small"
            />
          </Card>
        </Col>
        <Col xs={24} lg={8}>
          <Card title="Quick Actions">
            <Space direction="vertical" style={{ width: '100%' }}>
              <Card.Grid style={{ width: '100%', textAlign: 'center' }}>
                <CustomerServiceOutlined style={{ fontSize: '24px', color: '#1890ff' }} />
                <div>Add New Customer</div>
              </Card.Grid>
              <Card.Grid style={{ width: '100%', textAlign: 'center' }}>
                <UserOutlined style={{ fontSize: '24px', color: '#52c41a' }} />
                <div>Add New Employee</div>
              </Card.Grid>
              <Card.Grid style={{ width: '100%', textAlign: 'center' }}>
                <CalendarOutlined style={{ fontSize: '24px', color: '#faad14' }} />
                <div>Review Leave Requests</div>
              </Card.Grid>
            </Space>
          </Card>
        </Col>
      </Row>
    </div>
  );

  const renderContent = () => {
    switch (selectedKey) {
      case 'dashboard':
        return renderDashboard();
      case 'customers':
        return <div>Customers Module - Coming Soon</div>;
      case 'leads':
        return <div>Leads Module - Coming Soon</div>;
      case 'employees':
        return <div>Employees Module - Coming Soon</div>;
      case 'departments':
        return <div>Departments Module - Coming Soon</div>;
      case 'attendance':
        return <div>Attendance Module - Coming Soon</div>;
      case 'leave-requests':
        return <div>Leave Requests Module - Coming Soon</div>;
      default:
        return renderDashboard();
    }
  };

  return (
    <ConfigProvider
      theme={{
        token: {
          colorPrimary: '#1890ff',
          borderRadius: 8,
        },
      }}
    >
      <Layout style={{ minHeight: '100vh' }}>
        <Sider 
          collapsible 
          collapsed={collapsed} 
          onCollapse={setCollapsed}
          style={{
            background: '#fff',
            boxShadow: '2px 0 8px rgba(0,0,0,0.1)',
          }}
        >
          <div style={{ 
            height: '64px', 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'center',
            borderBottom: '1px solid #f0f0f0',
            fontSize: collapsed ? '16px' : '18px',
            fontWeight: 'bold',
            color: '#1890ff'
          }}>
            {collapsed ? 'CRM' : 'CRM + HRMS Pro'}
          </div>
          <Menu
            mode="inline"
            selectedKeys={[selectedKey]}
            items={menuItems}
            onClick={({ key }) => setSelectedKey(key)}
            style={{ borderRight: 0, marginTop: '8px' }}
          />
        </Sider>
        
        <Layout>
          <Header style={{ 
            padding: '0 24px', 
            background: '#fff', 
            display: 'flex', 
            justifyContent: 'space-between', 
            alignItems: 'center',
            boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
            zIndex: 10
          }}>
            <Title level={4} style={{ margin: 0, color: '#262626' }}>
              {(() => {
                const found = menuItems.find(item => {
                  if (!item || typeof item === 'string') return false;
                  if ('key' in item && item.key === selectedKey) return true;
                  if ('children' in item && item.children) {
                    return item.children.some(child => 
                      child && typeof child !== 'string' && 'key' in child && child.key === selectedKey
                    );
                  }
                  return false;
                });
                return (found && typeof found !== 'string' && 'label' in found ? found.label : 'Dashboard') as string;
              })()}
            </Title>
            
            <Space size="large">
              <Tag color={backendStatus === 'connected' ? 'green' : 'red'}>
                API: {backendStatus}
              </Tag>
              <Badge count={5}>
                <BellOutlined style={{ fontSize: '18px', color: '#666' }} />
              </Badge>
              <Dropdown overlay={userMenu} placement="bottomRight">
                <Space style={{ cursor: 'pointer' }}>
                  <Avatar icon={<UserOutlined />} />
                  <Text>Admin User</Text>
                </Space>
              </Dropdown>
            </Space>
          </Header>
          
          <Content style={{ 
            margin: '24px', 
            padding: '24px', 
            background: '#f5f5f5',
            minHeight: 'calc(100vh - 112px)',
            borderRadius: '8px'
          }}>
            {renderContent()}
          </Content>
        </Layout>
      </Layout>
    </ConfigProvider>
  );
}

export default App;
