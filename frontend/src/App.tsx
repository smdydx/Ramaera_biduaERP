import React from 'react';
import { ConfigProvider, Layout, Typography, Card, Row, Col } from 'antd';
import { UserOutlined, TeamOutlined, DashboardOutlined } from '@ant-design/icons';
import './App.css';

const { Header, Content } = Layout;
const { Title, Text } = Typography;

function App() {
  return (
    <ConfigProvider>
      <Layout style={{ minHeight: '100vh' }}>
        <Header style={{ background: '#001529', padding: '0 24px' }}>
          <div style={{ color: 'white', fontSize: '18px', fontWeight: 'bold' }}>
            CRM + HRMS Professional System
          </div>
        </Header>
        <Content style={{ padding: '24px', background: '#f0f2f5' }}>
          <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
            <Title level={2} style={{ textAlign: 'center', marginBottom: '32px' }}>
              Welcome to Professional CRM + HRMS System
            </Title>
            <Row gutter={[24, 24]}>
              <Col xs={24} sm={12} lg={8}>
                <Card 
                  hoverable
                  style={{ textAlign: 'center', height: '200px' }}
                  cover={<DashboardOutlined style={{ fontSize: '48px', color: '#1890ff', marginTop: '24px' }} />}
                >
                  <Card.Meta 
                    title="Dashboard" 
                    description="View analytics and system overview"
                  />
                </Card>
              </Col>
              <Col xs={24} sm={12} lg={8}>
                <Card 
                  hoverable
                  style={{ textAlign: 'center', height: '200px' }}
                  cover={<TeamOutlined style={{ fontSize: '48px', color: '#52c41a', marginTop: '24px' }} />}
                >
                  <Card.Meta 
                    title="CRM Module" 
                    description="Manage leads, customers, and sales pipeline"
                  />
                </Card>
              </Col>
              <Col xs={24} sm={12} lg={8}>
                <Card 
                  hoverable
                  style={{ textAlign: 'center', height: '200px' }}
                  cover={<UserOutlined style={{ fontSize: '48px', color: '#fa8c16', marginTop: '24px' }} />}
                >
                  <Card.Meta 
                    title="HRMS Module" 
                    description="Employee records, attendance, and leave management"
                  />
                </Card>
              </Col>
            </Row>
            <div style={{ textAlign: 'center', marginTop: '48px' }}>
              <Text type="secondary">
                Professional MNC-style system built with React + FastAPI
              </Text>
            </div>
          </div>
        </Content>
      </Layout>
    </ConfigProvider>
  );
}

export default App;