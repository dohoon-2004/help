/* ✅ 페이지네이션 영역만 타겟 */
.pager [data-testid="stHorizontalBlock"]{
  display: flex !important;
  flex-direction: row !important;
  flex-wrap: nowrap !important;
  justify-content: center !important;
  gap: 6px !important;              /* 간격 */
  margin-top: 10px !important;
}

/* 각 컬럼 폭 고정 */
.pager [data-testid="column"]{
  min-width: 42px !important;
  width: 42px !important;
  max-width: 42px !important;
  flex: 0 0 42px !important;
  padding: 0 !important;
  margin: 0 !important;
}

/* 숫자 버튼 원형 고정 */
.pager button{
  width: 42px !important;
  height: 42px !important;
  min-height: 42px !important;
  border-radius: 999px !important;   /* ✅ 원형 확정 */
  padding: 0 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  background: var(--card) !important;
  border: 1px solid var(--border) !important;
  box-sizing: border-box !important;
}

.pager button p{
  font-size: 1.10rem !important;
  font-weight: 800 !important;
  margin: 0 !important;
  color: var(--text) !important;
}

/* 선택된 페이지 */
.pager button[kind="primary"]{
  background: var(--page-primary) !important;
  border: none !important;
}
.pager button[kind="primary"] p{
  color: #ffffff !important;
}
