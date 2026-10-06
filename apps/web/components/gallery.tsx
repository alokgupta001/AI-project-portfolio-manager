"use client";
import { useState } from "react";
import {
  Badge,
  Button,
  ChartFrame,
  ConfirmDialog,
  DataTable,
  Field,
  MetricCard,
  Modal,
  Skeleton,
  StatePanel,
  type Confirmation,
} from "./ui";
const examples = [
  { id: "1", name: "Portfolio planning", state: "Ready", value: 8 },
  { id: "2", name: "Delivery review", state: "In review", value: 5 },
  { id: "3", name: "Resource planning", state: "Pending", value: 3 },
  { id: "4", name: "Governance review", state: "Ready", value: 6 },
  { id: "5", name: "Risk workshop", state: "Pending", value: 2 },
  { id: "6", name: "Benefits review", state: "In review", value: 4 },
];
export function Gallery() {
  const [drawer, setDrawer] = useState(false);
  const [confirm, setConfirm] = useState<Confirmation | null>(null);
  const [notice, setNotice] = useState("");
  return (
    <>
      <section className="page-heading">
        <div>
          <p className="eyebrow">DEVELOPMENT REFERENCE</p>
          <h1>Component gallery</h1>
          <p className="lead">
            Shared patterns for a consistent workspace. All records below are
            illustrative examples, not organization data.
          </p>
        </div>
        <Badge>Examples only</Badge>
      </section>
      <div className="metrics-grid">
        <MetricCard
          label="Example work items"
          value="28"
          detail="Illustrative count · not live portfolio data"
        />
        <MetricCard
          label="Example data coverage"
          value="Unknown"
          detail="Missing evidence is never treated as zero"
        />
        <MetricCard
          label="Example status"
          value={<Badge tone="warning">In review</Badge>}
          detail="Status is conveyed with text and color"
        />
      </div>
      <section className="panel">
        <h2>Table, filters & pagination</h2>
        <DataTable
          rows={examples}
          rowKey={(r) => r.id}
          caption="Example activities"
          searchText={(r) => `${r.name} ${r.state}`}
          columns={[
            {
              key: "name",
              label: "Activity",
              sort: (r) => r.name,
              render: (r) => r.name,
            },
            {
              key: "state",
              label: "Status",
              sort: (r) => r.state,
              render: (r) => <Badge>{r.state}</Badge>,
            },
            {
              key: "value",
              label: "Items (count)",
              sort: (r) => r.value,
              render: (r) => r.value,
            },
          ]}
        />
      </section>
      <div className="home-grid">
        <section className="panel">
          <h2>Forms & overlays</h2>
          <form
            className="identity-form"
            onSubmit={(e) => {
              e.preventDefault();
              setNotice("Example saved in this view only.");
            }}
          >
            <Field
              label="Example view name"
              hint="This demonstration does not persist data."
            >
              <input required maxLength={60} />
            </Field>
            <Button>Save example</Button>
          </form>
          {notice && <p role="status">{notice}</p>}
          <div className="actions">
            <Button variant="secondary" onClick={() => setDrawer(true)}>
              Open example drawer
            </Button>
            <Button
              variant="danger"
              onClick={() =>
                setConfirm({
                  title: "Discard example?",
                  description:
                    "Only this example message will be cleared. No organization data changes.",
                  confirm: async () => setNotice(""),
                })
              }
            >
              Discard example
            </Button>
          </div>
        </section>
        <ChartFrame
          title="Example activity distribution"
          description="Illustrative work item counts by activity; same values are available in the table."
          table={
            <table>
              <caption>Example distribution, items (count)</caption>
              <thead>
                <tr>
                  <th scope="col">Activity</th>
                  <th scope="col">Items</th>
                </tr>
              </thead>
              <tbody>
                {examples.slice(0, 3).map((r) => (
                  <tr key={r.id}>
                    <td>{r.name}</td>
                    <td>{r.value}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          }
        >
          <div className="example-bars">
            {examples.slice(0, 3).map((r) => (
              <div key={r.id}>
                <span>{r.name}</span>
                <div style={{ width: `${r.value * 10}%` }} />
                <b>{r.value}</b>
              </div>
            ))}
          </div>
        </ChartFrame>
      </div>
      <div className="home-grid">
        <StatePanel title="No records yet">
          Create a record when the owning module becomes available.
        </StatePanel>
        <StatePanel kind="forbidden" title="Access restricted">
          An organization Admin can help with membership permissions.
        </StatePanel>
        <StatePanel
          kind="error"
          title="Example request failed"
          action={
            <Button
              variant="secondary"
              onClick={() =>
                setNotice("Example retry acknowledged; no request was sent.")
              }
            >
              Try example again
            </Button>
          }
        >
          A failed request preserves the user's work and offers a clear next
          step.
        </StatePanel>
        <StatePanel kind="partial" title="Partial or stale data">
          Show coverage and freshness explicitly. Reload before editing a stale
          record.
        </StatePanel>
      </div>
      <section className="panel">
        <h2>Loading pattern</h2>
        <Skeleton label="Example loading state" />
      </section>
      <Modal
        open={drawer}
        onClose={() => setDrawer(false)}
        title="Example detail"
        drawer
      >
        <Badge>Illustrative</Badge>
        <h3>Evidence belongs beside decisions</h3>
        <p>
          Later modules can use this drawer for authorized details and source
          references.
        </p>
      </Modal>
      <ConfirmDialog value={confirm} onClose={() => setConfirm(null)} />
    </>
  );
}
